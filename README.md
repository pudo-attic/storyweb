# Grano StoryWeb

This is an implementation of text-snippet based SNA; the idea that data
in a social network isn't necessarily well-structured but can also be 
little pieces of text that link to each other (and to entities) through
a Markdown-like syntax.

Original mockup: [here](http://opendatalabs.org/misc/grano/_mockup).

This app is an experiment in whether such a semi-structured approach to 
influence and story mapping can be used to capture the building blocks 
of journalistic investigations.

## Domain model

Not yet. But hope dies last.


## Installation

...

To create a new database, run the following command: 

    python storyweb/manage.py initdb

This will also create an admin user with the email address ``admin@grano.cc`` and the password ``admin`` which you can use to log in and create more users.
