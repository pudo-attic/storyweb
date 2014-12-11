# Grano StoryWeb

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/granoproject/storyweb)

Journalism is about more than just storytelling: it's about weaving a narrative from a collection of facts that may often seem unrelated at first glance.
Storyweb is a tool for journalists to structure these facts, letting them explore the connections between findings from their own research and that of other team members. 

While the idea of structured journalism has been around for a while, Storyweb is an experiment in how tightly we can join the process of collecting and selecting rich, networked research data with the process of actually writing a story.

Storyweb creates a journalistic memory that can be pre-populated with a news organization's own archives and selected public data from governments and companies. Once it's up and running, this database can be shared inside a research team, making it possible for journalists to work better together.

---

This is an implementation of text-snippet based SNA; the idea that data
in a social network isn't necessarily well-structured but can also be 
little pieces of text that link to each other (and to entities).

Original mockup: [here](http://opendatalabs.org/misc/demo/grano/_mockup).

## Installation

Before you can install ``storyweb``, the following dependencies are required:

* A SQL database. While we recommend Postgres, the app can also run with other databases, such as SQLite.
* ElasticSearch for full-text indexing.
* ``less``, installed via ``npm``.
* Python, and Python ``virtualenv``.
* RabbitMQ

Once these dependencies are satisfied, run the following command to install the application:

    git clone https://github.com/granoproject/storyweb.git storyweb
    cd storyweb
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop
    npm install -g bower uglify-js

Next, you need to customize the configuration file. Copy the template configuration file, ``settings.py.tmpl`` to a new file, e.g. ``settings.py`` in the project root and set the required settings. Then export the environment variable ``TMI_SETTINGS`` to point at this file:

    cp settings.py.tmpl settings.py
    export STORYWEB_SETTINGS=`pwd`/settings.py

Use bower to install javascript dependencies:

    bower install

To create a new database, run the following command: 

    python storyweb/manage.py initdb

This will also create an admin user with the email address ``admin@grano.cc`` and the password ``admin`` which you can use to log in and create more users.

Congratulations, you've installed ``storyweb``. You can run the application using:

    python storyweb/manage.py runserver


## Credits

This tool is heavily inspired by [Newsclip.se](http://canvas.challengepost.com/submissions/30703-newsclip-se), a hack from the Al Jazeera "[Media in Context](http://canvas.aljazeera.com/)" hackathon in December 2014. Thanks to the team: Eva Constantaras, Kasia Dybek, Bruno Faviero, Heinze Havinga, Friedrich Lindenberg, Phillip Smith.

It is licensed under an open source MIT license. We welcome any contributions to the code base.
