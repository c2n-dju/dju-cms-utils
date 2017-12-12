#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from cmsplugin_filer_image.models import FilerImage as L1 # CMSPlugin
from djangocms_picture.models import Picture as L2 # CMSPlugin
from djangocms_text_ckeditor.models import Text
from djangocms_text_ckeditor.cms_plugins import TextPlugin
import djangocms_text_ckeditor as cke
from cms.api import add_plugin
from django.db import transaction

from cms.models.placeholdermodel import Placeholder

"""
a1 = L1.objects.all()


"""

def check_FilerImage(a1):
    """
    https://github.com/divio/cmsplugin-filer/blob/1.1.3/cmsplugin_flier_image/models.py#L21
    """

    # contrôle de la simplicité
    assert(len(set(map(lambda x: x.cmsplugin_ptr.id, a1))) == len(a1))
    assert(set(map(lambda x: x.style, a1)) == set((u'',)))
    assert(set(map(lambda x: x.caption_text, a1)) == set((u'',))) # paresseux
    assert(set(map(lambda x: x.image_url, a1)) == set((u'',))) # paresseux
    print(set(map(lambda x: x.alt_text, a1))) # IMPORTANT
    assert(set(map(lambda x: x.use_original_image, a1)) == set((False,)))
    assert(set(map(lambda x: x.use_autoscale, a1)) == set((False,)))
    print(sorted(set(map(lambda x: x.width, a1)))) # IMPORTANT
    print(sorted(set(map(lambda x: x.height, a1)))) # IMPORTANT
    assert(set(map(lambda x: x.crop, a1)) == set((True,)))
    assert(set(map(lambda x: x.upscale, a1)) == set((True,)))
    assert(set(map(lambda x: x.alignment, a1)) == set((None,)))
    assert(set(map(lambda x: x.free_link, a1)) == set((u'',)))
    assert(set(map(lambda x: x.original_link, a1)) == set((False,)))
    assert(set(map(lambda x: x.description, a1)) == set((u'',))) # paresseux
    assert(set(map(lambda x: x.target_blank, a1)) == set((False,)))
    assert(set(map(lambda x: x.file_link, a1)) == set((None,)))
    print(sorted(set(map(lambda x: x.image, a1)))) # IMPORTANT
    assert(set(map(lambda x: x.page_link, a1)) == set((None,)))
    assert(set(map(lambda x: x.thumbnail_option, a1)) == set((None,)))
    assert(set(map(lambda x: len(x.link_attributes), a1)) == set((0,)))

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

def move_one(l1):
    placeholder = l1.placeholder
    parent = l1.parent
    position = l1.position
    language = l1.language
    creation_date = l1.creation_date
    changed_date = l1.changed_date
    alt_text = l1.alt_text
    width = l1.width
    height = l1.height
    image = l1.image
    l1.delete()
    l2 = add_plugin(placeholder, 'PicturePlugin', language, position, parent,
                    width=width, height=height, picture=image, attributes={'alt':alt_text})


def copy_one(texts, oldnew, l1):
    placeholder = l1.placeholder
    parent = l1.parent
    position = l1.position
    language = l1.language
    creation_date = l1.creation_date
    changed_date = l1.changed_date
    alt_text = l1.alt_text
    width = l1.width
    height = l1.height
    image = l1.image
    print(image)
    # la position n'a probablement aucune importance
    l2 = add_plugin(placeholder, 'PicturePlugin', language, 'last-child', parent,
                    width=width, height=height, picture=image, attributes={'alt':alt_text})
    assert(not oldnew.has_key(l1.id))
    oldnew[l1.id] = l2.id
    texts.add(parent)


def rename_plugins(oldnew, tt):
    t = tt.djangocms_text_ckeditor_text
    pa = t.placeholder.page
    if pa == None:
        print("NO PAGE for " + t.placeholder.slot)
        return
    try:
        url = pa.get_absolute_url()
    except:
        url = "NO URL"   
    print(pa.get_admin_tree_title(), url, t.placeholder.slot)
    b = t.body
    plugs = cke.utils.get_plugins_from_text(b)
    didi = dict()
    for i in plugs.keys():
        if oldnew.has_key(i):
            didi[i] = oldnew[i]
        else:
            didi[i] = i
    b2 = cke.utils.replace_plugin_tags(b, didi)
    t.body = b2
    t.save()

@transaction.atomic
def migrate_images():
    a1 = L1.objects.all()
    check_FilerImage(a1)
    a2 = L2.objects.all()
    check_Picture(a2)
    lnop = []
    lstrange = []
    ltext = []
    for l1 in a1:
        if l1.parent == None:
            lnop.append(l1)
        elif l1.parent.plugin_type == u'TextPlugin':
            ltext.append(l1)
        else:
            lstrange.append(l1)

    assert(len(lnop) == 0)
    assert(len(lstrange) == 0)
    
    print("\nNow moving images in standard placeholders")
    for l1 in lnop:
        move_one(l1)
        
    print("\nNow creating new images for texts")
    texts = set()
    oldnew = dict()
    for l1 in ltext:
        copy_one(texts, oldnew, l1)
    texts = list(texts)

    print("\nNow moving images in texts")
    for tt in texts:
        rename_plugins(oldnew, tt)

    print("\nNow removing old images")
    for l1 in ltext:
        print(l1.id)
        l1.delete()

migrate_images()

"""
at = Text.objects.all()
for i,t in enumerate(at):
    if t.body.find("Route de Nozay, 91460 Marcoussis, France") >= 0 and\
       t.body.find("Fax") >= 0:
       pa = t.placeholder.page
       if pa != None and not pa.publisher_is_draft:
           print(i, pa.get_absolute_url(language='fr'), pa.get_absolute_url(language='en'))

p260 = at[260].placeholder.page # fr
p264 = at[264].placeholder.page # en
from cms.models.pagemodel import Page
from cms.models.pagemodel import PageMetaClass
from cms.models.titlemodels import Title
tis = Title.objects.filter(title="Practical informations")
ti1 = tis[0]
ti2 = tis[1]

tifra = Title.objects.get(page=p260,language='fr')
tiena = Title.objects.get(page=p260,language='en')

tifrb = Title.objects.get(page=p264,language='fr')
tienb = Title.objects.get(page=p264,language='en')

plugins = p260.placeholders.get(slot="content").get_plugins().filter(plugin_type="TextPlugin")
tps = map(lambda x:x.djangocms_text_ckeditor_text, plugins)
tefr = tps[0]
teen = tps[3]






cke.utils.OBJ_ADMIN_RE

"""
