Overview
======

This is the code for the Adult Education Platform and Matchmaker developed by Code for Canada in partnership with the Ministry of Advanced Education and Skills Development, the Ministry of Education and the Ministry of Citizenship and Immigration.

The setup documentation can be found below.

Tech stack
======
Python (2.7.14)<br />
PostgreSQL (10.4)<br />
Django (1.11)<br />
Vue.js (2.5.16)<br />

Django packages:<br />
• [Model translation](https://djangopackages.org/packages/p/django-modeltranslation/) (0.12.2)<br />
• [Smart selects](https://djangopackages.org/packages/p/django-smart-selects/) (1.5.4)<br />
• [Easy PDF](https://djangopackages.org/packages/p/django-easy-pdf/) (0.1.1)<br />
• [Widget tweaks](https://djangopackages.org/packages/p/django-widget-tweaks/) (1.4.2)<br />

Setup
======
In order to run the project you will need to download and/or install the software and packages specified above. Follow this guide to get you started. 

#### Python ####
Python 3 is the most recent version of the programming language but Python 2 comes preinstalled in most Linux distributions and is available as a package in all others. Furthermore, there are third-party libraries and packages that are still not compatible with Python 3 as of today. We will be using Python 2.7 in particular because most recent versions of Macs come with it preinstalled. If Python is not preinstalled in your computer, get Python 2.7.14 (released in September 2017) [here](https://www.python.org/downloads/) or with your operating system's package manager. <br />


#### PostgreSQL ####

[Here](https://wiki.postgresql.org/wiki/Detailed_installation_guides) you can find a list of detailed PostgreSQL installation guides for different operating systems. <br />
For Mac OS X, I recommend installing PostgreSQL via [Homebrew](https://brew.sh/) by running two commands:

    brew update
    brew install postgresql
Follow the instructions at the end of the install to initialize the DB, add startup items, and start PostgreSQL. <br />

#### Django ####
The official Django [docs](https://docs.djangoproject.com/en/1.11/topics/install/) provide detailed instructions on how to install Django. We will use Django 11.1 (released in April 2017) because it is the latest Django version that works with Python 2.7.

#### Vue.js ####
[Here](https://vuejs.org/v2/guide/installation.html) are the installation guides of Vue.js. In this project we're using the direct `<script>` include for Vue.js 2.5.16 (released in March 2018).
