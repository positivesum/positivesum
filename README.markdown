## Introduction
Positive Sum is a Python library that provides functions that simplify +∑ Positive Sum development process.

## Installation

1. With easy_install or distribute install pip

    sudo easy_install pip

2. With pip install Fabric

    sudo pip install fabric

3. With pip install positivesum package

    sudo pip install positivesum

## How to use *positivesum* package in a project?
*positivesum* package provides Fabric functions that can be executed on an +∑ Positive Sum project. These functions are
typically included in the project's fabfile.py. To see if the project already has an existing fabfile.py, go into the
project's root directory and check if fabfile.py exists. If it already exists, then you should be able to execute
*fab --list* to get a list of available project functions.

## How to include *positivesum* functionality in a project?
To include *positivesum* functionality in a project, create a *fabfile.py* file in the project's root directory.
fabfile.py is a Python script, therefore it must follow Python syntax and Python conventions.

For a fabfile to be useful, it must have at least 1 *positivesum* function. To include a *positivesum* function in a
project, you must import a Python function from the *positivesum* package into the fabfile. For example, to add the
migrate function from the *positivesum* package you would add the following code to the top of the script:

    from positivesum.mysql import migrate

After this, you should be able to see migrate option available when executing "fab --list" inside of the project
directory.

## Functions

### migrate
*migrate* function generates a migration script that will migrate a database from one url to another. It has some
predefined parameters and requires some parameters. The simplest examples of executing the migrate function is

    fab migrate:from_url=http://projecturl,to_url=http://projecturl.ps.hstd.org

This command includes 2 parameters: _from_url_ and _to_url_. All other parameters are assumed. It assumes that the
database dump is in *db/last* and that the output should be written to *db/migration.sql*. You can overwrite these
options by explicitly indicating these parameters for example

    fab migrate:from_url=http://projecturl,to_url=http://projecturl.ps.hstd.org,db_dump=/path/to/dump/file,output=/path/to/output

### generate
*generate* function produces a tarball of a project for a specific url. To generate a package you must specify what
environment this package is for and what url you are migrating from.

    fab live generate:from_url=http://projecturl

### update
*update* function updates a specific environment with the latest version from the git repository.

    fab demo update

