from __future__ import with_statement

from fabric.api import require, local, env, prompt, run
from fabric.context_managers import cd
import os, tempfile
from positivesum.db import mysql
from positivesum.utilities import compile_excludes

def generate(from_url=None, to_url=None, version=None, output=None):
    '''
    Generate deployment package
    '''

    require('exclude')

    # create tmp directory
    tmpd = tempfile.mkdtemp()

    # create html directory
    local('mkdir %s/html'%tmpd)

    # create db directory
    local('mkdir %s/db'%tmpd)

    # copy files to this directory
    local('rsync -av html/ %s/html/ --exclude=%s'%(tmpd, ' --exclude='.join(compile_excludes())))

    # create database migration script
    if not from_url:
        from_url = prompt('Url to migrate from?')
    if not to_url:
        to_url = env.site_url

    migration_dump = os.path.join(tmpd,'db','migration.sql')

    mysql.migrate(from_url, to_url, output=migration_dump)

    # migrate the database
    tmp_db = mysql.create_tmp_db()
    local('mysql %s < db/last'%tmp_db)
    local('mysql %s < %s'%(tmp_db, migration_dump))
    local('rm %s'%migration_dump)

    # dump migrated database
    local('mysqldump --default-character-set=utf8 %s > %s/db/last'%(tmp_db, tmpd))

    # create CHANGELOG
    # TODO: generate change log from PivotalTracker stories
    changelog = "CHANGELOG generation will be included in final version of the WordPress Package Generator"
    local('echo "%s" > %s'%(changelog, os.path.join(tmpd, 'CHANGELOG')))

    # copy TESTS
    if os.path.exists('tests.txt'):
        local('cp tests.txt %s'%os.path.join(tmpd, 'tests.txt'))

    # write version file
    if not version:
        version = prompt('What should I call this version?')
        local('echo %s > %s'%(version, os.path.join(tmpd, 'VERSION')))

    # create tar.gz
    if not output:
        output = '.'

    tarball = "%s-%s-%s.tar.gz"%(env.project, env.name, version)
    output = os.path.join(output, tarball)

    local('tar -C %s -pczf %s .'%(tmpd, output))

def update():
    '''
    Update a site with the latest version from git repository
    '''
    require('site_path')
    require('name')

    with(cd(env.site_path)):
        run('git pull origin master')
