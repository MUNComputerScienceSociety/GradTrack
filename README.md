# GradTrack

A graduation scheduling system that helps students plan their courses

## Goal

**From the hackathon ideas list:**

>Keeping track of the requirements a student must fulfill in order to graduate can be somewhat 
>painful due to the strucutre of self-serve and the density of the information in the university calendar.
>Providing students with a simple interface to help them track their progression towards graduating would 
>make it substantially easier to plan for upcoming semesters. Software such as this could be extended to
>automatically populate a set of requirements based on a specified degree type (e.g. [B.Sc, Major in Comp.
>Sci, Minor in Math]), and could also potentially make course suggestions referrencing annual offerings 
>using the API mentioned above.

## Implementation

### Scraper

A mechanism will have to be created to, ideally automatically, fetch course information en masse.
Course information and graduation requirements should be updated fairly regularly and be easily
accessible from the main application. To accomplish this, a 
[web scraper](http://en.wikipedia.org/wiki/Web_scraping) should be implemented in the
[Python (version 2.7)](https://wiki.python.org/moin/BeginnersGuide/Programmers) programming language,
which is used in a number of courses at Memorial University.

### Main Application

The main application is a web application implemented in [Node.js](http://nodejs.org/), which is being
used in the Software Methodologies and Team Project courses.  The appliation should focus on interactions
through a calendar interface and update dynamically. The [Express](http://expressjs.com/) framework is 
used for handling the generic requirements of a web application, such as routing and templating.  Note that
[Embedded Javascript](http://www.embeddedjs.com/) templates are used here instead of the default.

## Directory Structure

    GradTrack
    ├── app
    |   ├── app.js
    |   ├── package.json
    |   ├── bin
    |   ├── public
    |   |   ├── stylesheets
    |   |   ├── javascripts
    |   |   └── images
    |   ├── routes
    |   └── views
    ├── util
    |   └── scraper.py
    ├── .gitignore
    ├── LICENSE
    └── README.md

The `app` directory contains the code and resources for the application. `app.js` is the main Javascript
file responsible for configuring the server and assigning branches of the route handlers. `package.json`
is used to configure information about the application and list dependencies. The `bin` directory can be
ignored. Clearly, `public` contains directories to house stylesheets, javascript files, and images for
the application. The `routes` directory contains javascript files corresponding to each major branch of
the application's routing table, and each route file implements handlers for subroutes. The `views`
directory houses template markup files (EJS + HTML) and each view has a `.ejs` extension. The `util`
directory houses utilities for such tasks as web scraping to gather course information. Whenever the 
directory structure or set of instructions required to configure and run the application change, the new
information should be reflected in `README.md`. Whenever new dependencies are required by the application,
they must be lsited in `package.json`.

## Execution

To execute the application, navigate to the `app` directory and execute

    npm install
    npm start

And then navigate to `localhost:3000` in your browser to visit the index page.

However, note that `npm install` need only be run:

1. The first time you start the application and
2. Whenever the list of dependencies in `package.json` change.