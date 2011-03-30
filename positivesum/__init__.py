from fabric.api import env
import os

class Environment:

    def __init__(self, name, exclude, site_url, locked_db=True, site_path=None, host='localhost'):
        self.name = name
        self.exclude = exclude
        self.site_url = site_url
        self.site_path = site_path
        self.locked_db = locked_db
        self.__doc__ = self.site_url
        self.host_string = host

    def __call__(self):
        env.project = os.getcwd().split('/')[-1]
        env.name = self.name
        env.exclude = self.exclude
        env.site_url = self.site_url
        env.locked_db = self.locked_db
        env.site_path = self.site_path
        env.host_string = self.host_string