# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db.models import SmallIntegerField

DAY_OF_THE_WEEK = {
    '1' : _(u'Monday'),
    '2' : _(u'Tuesday'),
    '3' : _(u'Wednesday'),
    '4' : _(u'Thursday'),
    '5' : _(u'Friday'),
    '6' : _(u'Saturday'), 
    '7' : _(u'Sunday'),
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)

CLB_LEVEL = {
    '1' : _(u'1'),
    '2' : _(u'2'),
    '3' : _(u'3'),
    '4' : _(u'4'),
    '5' : _(u'5'),
    '6' : _(u'6'), 
    '7' : _(u'7'),
    '8' : _(u'8'),
    '9' : _(u'9'),
}

class CLBField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(CLB_LEVEL.items()))
        kwargs['max_length']=1 
        super(CLBField, self).__init__(*args, **kwargs)        