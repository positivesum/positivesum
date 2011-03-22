from fabric.api import env
import os

class Environment:

    def __init__(self, name, exclude, site_url, locked_db=True):
        self.name = name
        self.exclude = exclude
        self.site_url = site_url
        self.locked_db = locked_db
        self.__doc__ = self.site_url

    def __call__(self):
        env.project = os.getcwd().split('/')[-1]
        env.name = self.name
        env.exclude = self.exclude
        env.site_url = self.site_url
        env.locked_db = self.locked_db