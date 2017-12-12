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


def check_Picture(a2):
    """
    https://github.com/divio/djangocms-picture/blob/2.0.5/djangocms_picture/models.py#L57
    """

    # contrôle de la simplicité
    assert(len(set(map(lambda x: x.cmsplugin_ptr.id, a2))) == len(a2))
    print(sorted(set(map(lambda x: x.link_url, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.alignment, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.link_page, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.height, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.width, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.picture, a2)))) # IMPORTANT
    print(sorted(set(map(lambda x: str(x.attributes), a2))))
    assert(set(map(lambda x: x.link_target, a2)) == set((u'',))) # paresseux
    print(sorted(set(map(lambda x: x.use_automatic_scaling, a2)))) # IMPORTANT
    assert(set(map(lambda x: x.use_crop, a2)) == set((False,)))
    assert(set(map(lambda x: x.use_no_cropping, a2)) == set((False,)))
    assert(set(map(lambda x: x.use_upscale, a2)) == set((False,)))
    print(sorted(set(map(lambda x: x.thumbnail_options, a2)))) # IMPORTANT
    assert(set(map(lambda x: x.external_picture, a2)) == set((u'',))) # paresseux
    print(sorted(set(map(lambda x: x.external_picture, a2)))) # IMPORTANT
    assert(set(map(lambda x: x.template, a2)) == set((u'default',))) # paresseux


a2 = Picture.objects.all()
check_Picture(a2)

for l2 in a2:
    d = l2.attributes
    if d.has_key(u'alt') and d[u'alt'] == u'':
        d.pop(u'alt')
        l2.save()

a2 = Picture.objects.all()
check_Picture(a2)
