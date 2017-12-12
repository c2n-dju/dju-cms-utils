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

phs = Placeholder.objects.filter(slot="descriptif_departement")
new = "content"

for (old, new) in [("descriptif_departement", "content"), ("info_departement", "info"), ("uv", "content")]:
    phs = Placeholder.objects.filter(slot=old)
    for ph in phs:
        pa = ph.page
        if pa != None:
            print("renaming " + ph.slot + " from " + pa.get_absolute_url("en"))
        else:
            print("renaming " + ph.slot + " from no page")
        ph.slot = new
        ph.save()
