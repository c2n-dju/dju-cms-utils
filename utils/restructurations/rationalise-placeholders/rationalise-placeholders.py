#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from djangocms_picture.models import Picture
from djangocms_text_ckeditor.models import Text
from djangocms_text_ckeditor.cms_plugins import TextPlugin
import djangocms_text_ckeditor as cke
from cms.api import add_plugin
from django.db import transaction

from cms.models.placeholdermodel import Placeholder
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title

# https://gist.github.com/nicksnell/9228580 ATTENTION BUG Manque map slot dans template_placeholders
from django.template import TemplateDoesNotExist
from cms.models.pagemodel import Page
from cms.utils.plugins import get_placeholders

phs = Placeholder.objects.all()

for ph in phs:
    if len(ph.get_plugins_list()) > 0:
        continue
    pa = ph.page
    if pa == None:
        continue
    slots = map(lambda x:x.slot, get_placeholders(pa.get_template()))
    if not ph.slot in slots:
        print("deleting " + ph.slot + " from " + pa.get_absolute_url("en"))
        odel = ph.delete()
        if odel[0] != 2 or odel[1]['cms.Placeholder'] != 1 or odel[1]['cms.Page_placeholders'] != 1:
            print("OUILLE :")
            print(odel)

phs = Placeholder.objects.filter(slot='equipes')
mama = map(lambda x:len(x.get_plugins_list()), phs)
if len(mama) > 0 and max(mama) == 0:
    print('Removing all "equipes" placeholders, please remove {% placeholder "equipes" %} from templates')
    for ph in phs:
        odel = ph.delete()
        if odel[0] != 2 or odel[1]['cms.Placeholder'] != 1 or odel[1]['cms.Page_placeholders'] != 1:
            print("OUILLE :")
            print(odel)
