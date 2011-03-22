from subprocess import Popen, PIPE, STDOUT
from fabric.api import env
import os.path

def replace(value):
    '''
    Perform a string replace inside of string and return the result.
    Function handles serialized strings by deserializing them and performing recursively replacing strings inside of
    array values.
    '''
    location = os.path.dirname(__file__)
    command = '''php %(location)s %(from)s %(to)s'''%{'location':os.path.join(location, 'replace.php'),'from':env.from_url,'to':env.to_url}
    p = Popen(command.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    output, error = p.communicate(input=value)
    return output