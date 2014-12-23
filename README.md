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
through a calendar interface and update dynamically.
