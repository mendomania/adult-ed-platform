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

This code snippet was taken from the [models](https://github.com/mendomania/adult-ed-platform/blob/master/osr/models.py) file of this project. It defines a database table called `FutureMatch` with a foreign key (`goal`) to another table called `GoalPath`, two char fields (`code` and `text`), and a positive small integer field (`order_id`). Note how all strings in this class as tagged as translatable. Please refer to the <b>Translation</b> section below for more details on this.<br /><br /> 
The variables `verbose_name` and `help_text` refer to the strings that will be shown in the admin interface next to their corresponding  fields whenever a user performs any CRUD operation (create, read, update, delete) on the `FutureMatch` table through the admin interface (that is shown in the diagram as the window with the <b>Private</b> label under it). Please refer to the description of the admin file below for more details on this.<br /><br />
[Here](https://docs.djangoproject.com/en/2.1/topics/db/models/) are the official docs for models in Django.<br />

• <b>The admin file</b> (`admin.py`)<br />
Once the models file is created and the `migrate` and `makemigrations` commands are run (more on this below), Django will automatically provide an admin interface that works out-of-the-box and allows authenticated users to perform CRUD operations on database tables (note that groups and permissions can be created such that some users have access and CRUD permissions on only certain tables, more on this [here](https://docs.djangoproject.com/en/2.1/topics/auth/)).<br /><br />
The admin file can then be used to define `ModelAdmin` classes. These are representations of a model in the admin interface. In a nutshell, this file is used to customise the admin interface. For example, by deciding which fields of each model should even show up in this interface (perhaps there are fields that we don't want to show to users), to group together certain fields in a section with a specific label (so it's easier for users to go through the process of adding a new record in a certain table) or to make sure a certain user or group of users can only see the records they have created.

     class FutureMatchAdmin(TranslationAdmin):
       pass
     admin.site.register(FutureMatch, FutureMatchAdmin)  

This code snippet was taken from the [admin](https://github.com/mendomania/adult-ed-platform/blob/master/osr/admin.py) file of this project. Here you can see that for the `FutureMatch` table no special processing is done in the admin file, other than defining a subclass of the base class `TranslationAdmin` (which is part of the <b>django-modeltranslation</b> package) that is called `FutureMatchAdmin` and then registering `FutureMatch` to this `ModelAdmin` class.
<p align="center">
<img src="https://github.com/mendomania/adult-ed-platform/blob/master/example_admin.png" align="center">
</p>

Here is a screenshot of how this looks in the admin interface. Note how the four `FutureMatch` fields defined in the models section above show up in the admin interface with the `verbose_name` and `help_text` values that were defined. Also note how the char field `Text` appears twice, in English and in French. This is because it was tagged as a translatable field. Please refer to the <b>Translation</b> section below for more details on this.<br /><br />
[Here](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/) are the official docs for the Django admin interface.<br />

• <b>The URLs file</b> (`urls.py`)<br /><br />
• <b>The views file</b> (`views.py`)<br /><br />

#### Translation ####
• <b>The translation file</b> (`translation.py`)<br /><br />
• <b>The message file</b> (`django.po`)<br /><br />
• <b>The compiled version of the message file</b> (`django.mo`)<br /><br />

#### Useful commands ####
