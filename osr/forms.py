# -*- coding: utf-8 -*-
from django import forms

class OfferingForm(forms.ModelForm):
    print '------------------------'
    class Media:
        js = ('admin/js/offering_admin.js')
