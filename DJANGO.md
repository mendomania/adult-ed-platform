Django 101
======
#### Diagram ####
Here is a diagram of the most important Django files for this project. The section below will explain in more detail what they do and when you would need to make changes to them.
<p align="center">
<img src="https://github.com/mendomania/adult-ed-platform/blob/master/django101.png" align="center">
</p>

#### Python files ####
• <b>The settings file</b> (`settings.py`)<br />
This file contains all the configuration of a Django installation. It is composed of a series of variable definitions. Because it contains sensitive information, access to it should be limited. [Here](https://docs.djangoproject.com/en/2.1/topics/settings/) are the official docs for this file. These are some of the variables it contains:<br /><br />
• `INSTALLED_APPS`: A list of strings designating all applications that are enabled in this Django installation. All Django packages that are needed for a project will be listed here, for instance. For this project, you can see that `django-modeltranslation`, `django-smart-selects`, `django-easy-pdf` and `django-widget-tweaks` are listed in the [settings](https://github.com/mendomania/adult-ed-platform/blob/master/app/settings.py).<br /><br />
• `DATABASES`: A Python dictionary containing the settings for all databases to be used with Django. One `default` database must be specified. Other databases could then optionally be specified too. For this project, we only define the `default` database, and that is PostgreSQL. If you wanted to use a different data store with Django, here is where you would make the change. Note that the database permissions are also specified here.<br /><br />
• `LANGUAGES`: A list of all available languages that will be used for translation purposes. Once this setting is specified, any text that is tagged as translatable in the Python code or the HTML code (read more about this in the <b>Translation</b> section down below) will be included in a message file (that will have the `po` extension, this [file](https://github.com/mendomania/adult-ed-platform/blob/master/locale/fr/LC_MESSAGES/django.po) is the only message file needed for this project). Translations should then be manually added to this message file, and then it should be compiled. Once that is done, Django will take care of translating web apps on the fly in each available language, according to users' language preferences. This project supports English and French.

     # List of languages the web app supports
     LANGUAGES = (
       ('en', _('English')),
       ('fr', _('French')),
     )

• <b>The models file</b> (`models.py`)<br />
This file specifies the fields and behaviours of the data that we want to store. Each model maps to a single database table. In that way, this file defines the <b>database schema</b> for this project. Here is one example table, `FutureMatch`.
     
     @python_2_unicode_compatible
     class FutureMatch(models.Model):
       class Meta:
         verbose_name = _('future match')
         verbose_name_plural = _('future matches')  
         ordering = ['order_id']

       def __str__(self):
         return self.code 
    
       goal = models.ForeignKey(GoalPath, on_delete=models.CASCADE, verbose_name=_('goal path'))
       code = models.CharField(max_length=100, verbose_name=_('code'))
       text = models.CharField(max_length=500, verbose_name=_('text'))
       order_id = models.PositiveSmallIntegerField(verbose_name=_('order id'), default=1, 
         help_text=_('a lower order id will show up first, min value is 1'))    

This code snippet defines a database table called `FutureMatch` with a foreign key (`goal`) to another table called `GoalPath`, two char fields (`code` and `text`), and a positive small integer field (`order_id`). Note how all strings in this class as tagged as translatable. Please refer to the <b>Translation</b> section below for more details on this. The variables `verbose_name` and `help_text` refer to the strings that will be shown in the admin interface next to their corresponding  fields whenever a user performs any CRUD operation (create, read, update, delete) on the `FutureMatch` table through the admin interface (that is shown in the diagram as the window with the <b>Private</b> label under it). Please refer to the description of the admin file below for more details on this.

• <b>The translation file</b> (`translation.py`)<br /><br />

• <b>The admin file</b> (`admin.py`)<br /><br />
• <b>The URLs file</b> (`urls.py`)<br /><br />
• <b>The views file</b> (`views.py`)<br /><br />

#### Translation ####
• <b>The message file</b> (`django.po`)<br /><br />
• <b>The compiled version of the message file</b> (`django.mo`)<br /><br />
