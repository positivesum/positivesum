from fabric.api import env, local
import os

def smart_str(s, encoding='utf-8', errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in
    'encoding'.
    """
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def compile_excludes():
    '''
    Returns a list of all excludes
    '''
    exclude = env.exclude
    if os.path.exists('.gitignore'):
        gitignore = local('cat .gitignore', capture=True)
        exclude = exclude + gitignore.split('\n')
    return exclude
