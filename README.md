# Grano TMI

This is an implementation of text-snippet based SNA; the idea that data
in a social network isn't necessarily well-structured but can also be 
little pieces of text that link to each other (and to entities) through
a Markdown-like syntax.

Original mockup: [here](http://opendatalabs.org/misc/grano/_mockup).

This app is an experiment in whether such a semi-structured approach to 
influence and story mapping can be used to capture the building blocks 
of journalistic investigations.

## Installation

Before you can install ``tmi``, the following dependencies are required:

* A SQL database. While we recommend Postgres, the app can also run with other databases, such as SQLite.
* ElasticSearch for full-text indexing.
* ``less``, installed via ``npm``.
* Python, and Python ``virtualenv``.

Once these dependencies are satisfied, run the following command to install the application: 

    git clone https://github.com/pudo/tmi.git tmi
    cd tmi
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop

Next, you need to customize the configuration file. Copy the template configuration file, ``settings.py.tmpl`` to a new file, e.g. ``settings.py`` in the project root and set the required settings. Then export the environment variable ``TMI_SETTINGS`` to point at this file:

    cp settings.py.tmpl settings.py
    export TMI_SETTINGS=`pwd`/settings.py

To create a new database, run the following command: 

    python tmi/manage.py initdb

This will also create an admin user with the email address ``admin@grano.cc`` and the password ``admin`` which you can use to log in and create more users.

Next, you can load and index some example data:

    python tmi/manage.py load demo/economist.yaml
    python tmi/manage.py index

Congratulations, you've installed ``tmi``. You can run the application using:

    python tmi/manage.py runserver

