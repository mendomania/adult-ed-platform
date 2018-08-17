Django 101
======
Here is a diagram of the most important Django files for this project. The section below will explain in more detail what they do and when you would need to make changes to them.
<p align="center">
<img src="https://github.com/mendomania/adult-ed-platform/blob/master/django101.png" align="center">
</p>

• <b>The settings file</b> (`settings.py`)<br />
This file contains all the configuration of a Django installation. It is composed of a series of variable definitions. Because it contains sensitive information, access to it should be limited. These are some of the variables it contains:<br /><br />
• `INSTALLED_APPS`: A list of strings designating all applications that are enabled in this Django installation. All Django packages that are needed for a project will be listed here, for instance. For this project, you can see that `django-modeltranslation`, `django-smart-selects`, `django-easy-pdf` and `django-widget-tweaks` are listed in the [settings](https://github.com/mendomania/adult-ed-platform/blob/master/app/settings.py).<br /><br />
• `DATABASES`: A Python dictionary containing the settings for all databases to be used with Django. One `default` database must be specified. Other databases could then optionally be specified too. For this project, we only define the `default` database, and that is PostgreSQL. If you wanted to use a different data store with Django, here is where you would make the change. Note that the database permissions are also specified here.<br /><br />
• `LANGUAGES`: A list of all available languages that will be used for translation purposes. Once this setting is specified, any text that is tagged as translatable in the Python code or the HTML code (read more about this in the <b>Translation</b> section down below) will be included in a message file (that will have the `po` extension, this [file](https://github.com/mendomania/adult-ed-platform/blob/master/locale/fr/LC_MESSAGES/django.po) is the only message file needed for this project). Translations should then be manually added to this message file, and then it should be compiled. Once that is done, Django will take care of translating web apps on the fly in each available language, according to users' language preferences.<br/><br />
• <b>models.py</b>: A<br />
• <b>translation.py</b>: A<br />
• <b>admin.py</b>: A<br />
• <b>urls.py</b>: A<br />
• <b>views.py</b>: A<br />

• <b>django.po</b>: A<br />
• <b>django.mo</b>: A<br />
