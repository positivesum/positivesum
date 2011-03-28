from fabric.api import local, require, abort, env
import os, hashlib, datetime
import MySQLdb
from positivesum import php
from positivesum.utilities import smart_str

def migrate(from_url, to_url, db_dump='db/last', db_prefix='wp_', output='db/migration.sql', drop=True):
    '''
    Generate database dump file with fixed site url
    '''

    env.tables = _migration_tables()
    env.from_url = from_url
    env.to_url = to_url
    env.db_dump = db_dump
    env.db_prefix = db_prefix
    env.output = output

    # check to make sure that db_dump exists
    if not os.path.isabs(env.db_dump):
       env.db_dump = os.path.join(os.getcwd(), db_dump)

    # prepare the output path
    if type(env.output) == str:
        if not os.path.isabs(env.output):
            env.output = os.path.join(os.getcwd(), env.output)
        output = open(env.output, 'w')

    if not os.path.exists(env.db_dump):
        abort('Dump file does not exist in path %s'%env.db_dump)

    # create test database with test_{hash} name
    env.tmp_db = tmp_db = create_tmp_db()

    # import the database from database dump
    local('mysql %s < %s'%(tmp_db, env.db_dump))

    # foreach table replace url from to
    for table, callback, args in env.tables:
        output.write(callback(table, args))

    output.close()

    if drop:
        # drop test database we no longer need it
        local('mysql -e "drop database %s"'%tmp_db)

def create_tmp_db():
    '''
    Return name of a newly created database
    '''
    tmp_db = 'tmp_%s'%hashlib.md5(str(datetime.datetime.now())).hexdigest()[0:8]

    # create temporary test database
    local('mysql -e "create database %s"'%tmp_db)

    return tmp_db

def inline_replace(table, args):
    '''
    Return SQL statement for updating a simple string column using mysql REPLACE
    '''
    index, column = args

    format = '''
    /* Replace all occurrences of %(from)s to %(to)s in %(table)s.%(table)s */\n
    UPDATE %(table)s SET %(column)s = REPLACE(%(column)s,'%(from)s','%(to)s');\n
    '''
    values = {
        'table':env.db_prefix+table,
        'column':column,
        'to':env.to_url,
        'from':env.from_url
    }
    return format%values

def mixed_content(table, args):
    '''
    Return SQL statement for updating mixed content value
    '''
    index, column = args

    like_from = '%'+env.from_url+'%'
    table = env.db_prefix+table

    db = MySQLdb.connect(db=env.tmp_db, read_default_file='~/.my.cnf')
    c = db.cursor()
    query = '''SELECT %s, %s FROM %s WHERE %s LIKE '''%(index, column, table, column)
    c.execute(query + ' %s',(like_from,))

    output = []

    for row in c.fetchall():
        id, value = row
        replaced = php.replace(smart_str(value))
        output.append('''UPDATE %s SET %s=%s WHERE %s=%s;\n'''%\
                      (table, column, db.escape(replaced), index, id))

    return '\n'.join(output)

def _migration_tables():
    '''
    Return a dictionary of tables that should migrated
    TODO: Make it possible to overwrite these values
    '''

    tables = [
            ('options', mixed_content, ('option_id','option_value')),
            ('posts', inline_replace,  ('ID','post_content')),
            ('posts', inline_replace,  ('ID', 'guid')),
            ('postmeta', mixed_content, ('meta_id','meta_value')),
            ('icl_translation_status', mixed_content, ('translation_id', 'translation_package')),
            ('redirection_logs', inline_replace, ('id','referrer')),
            ('rg_lead', inline_replace, ('id','source_url')),
            ('links', inline_replace, ('link_id', 'link_image'))
    ]

    return tables