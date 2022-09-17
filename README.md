# Snow a simple web framework

This repository is an effort to understand how the web framework works. We started 
with a simple static page rendering engine until we arrived at a simple framework called Snow.

## First way with Pure Python 

The main goal of this repository is to study Python to develop a web application without any framework or external 
library just using built-in functions and classes of Python itself.

We'll follow these steps:

- create a database integration with SQLite that has a native Python integration;
- create templates for our HTML files that will be generated by our render script;
- create a render template script, this script catches the data on the database and mixes it with the HTML template to generate a respective HTML file. This script needs to be executed before publishing our website pages.
- create a simple server WSGI script that serves dynamically the HTML pages. With this simple server, we don't need to render the pages of our websites before publishing, but these pages will be generated dynamically.

## Second way with some libraries of Python ecosystem

After the first way, now we'll use some Python libraries to help us to build a robust application to render and serve our blog.

These libraries are on requirements.txt file.

We'll follow these steps:

- improve the app with Jinja2 template engine

## Third way is to convert the WSGI server to a Web Framework

After creating a static HTML render and migrating it to a simple WSGI dynamic server, now we improve our knowledge by 
converting the WSGI server to a simple Web Framework called Snow.

We followed these steps:

- Create a class called Snow, that is our framework
- Instantiate an app object from our class
- Create business rules in a specific module to decouple our logic from our implementation