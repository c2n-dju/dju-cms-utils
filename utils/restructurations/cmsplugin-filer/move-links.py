#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from cmsplugin_filer_link.models import FilerLinkPlugin as L1
from djangocms_link.models import Link as L2
from djangocms_text_ckeditor.models import Text
from djangocms_text_ckeditor.cms_plugins import TextPlugin
import djangocms_text_ckeditor as cke
from cms.api import add_plugin
from django.db import transaction

from cms.models.placeholdermodel import Placeholder

def check_FilerLinkPlugin(a1):
    """
    https://github.com/divio/cmsplugin-filer/blob/1.1.3/cmsplugin_filer_link/models.py#L27
    """
    tilt = False
    for l1 in a1:
        cmsplugin_ptr = l1.cmsplugin_ptr
        name = l1.name
        url = l1.url
        mailto = l1.mailto
        link_style = l1.link_style
        new_window = l1.new_window
        file = l1.file
        page_link = l1.page_link
        link_attributes = l1.link_attributes

        # contrôle de la pureté-simplicité
        if (url != "" and (mailto != ""  or page_link != None)) or\
           (mailto != "" and (url != ""  or page_link != None)) or\
           (page_link != None and (url != "" or mailto != "")):
            print('TILT!', cmsplugin_ptr, name, url, mailto, link_style, file, page_link, link_attributes)
            tilt = True
            # trucs pas compris
        if link_style != " " or file != None or link_attributes != {}:
            print('TILT!', cmsplugin_ptr, name, url, mailto, link_style, file, page_link, link_attributes)
            tilt = True
    return tilt


def check_Link(a2):
    """
    https://github.com/divio/djangocms-link/blob/2.1.2/djangocms_link/models.py#L48
    """
    tilt = False
    for l2 in a2:
        cmsplugin_ptr = l2.cmsplugin_ptr
        name = l2.name
        external_link = l2.external_link
        anchor = l2.anchor
        mailto = l2.mailto
        phone = l2.phone
        internal_link = l2.internal_link
        attributes = l2.attributes
        template = l2.template

        # contrôle de la pureté-simplicité
        if (external_link != "" and (mailto != "" or phone != "" or internal_link != None)) or\
           (mailto != "" and (external_link != "" or phone != "" or internal_link != None)) or\
           (internal_link != None and (mailto != "" or phone != "" or external_link != "")) or\
           (phone != "" and (external_link != "" or mailto != "" or internal_link != None)):
            print('TILT!', cmsplugin_ptr, name, external_link, anchor, mailto, phone, internal_link, attributes, template)
            tilt = True
        if (anchor != "" or attributes != {} or template != u"default"):
            print('TILT!', cmsplugin_ptr, name, external_link, anchor, mailto, phone, internal_link, attributes, template)
            tilt = True
    return tilt

# def check_FilerImagePlugin(a1):        

def move_one(l1):
    placeholder = l1.placeholder
    parent = l1.parent
    position = l1.position
    language = l1.language
    creation_date = l1.creation_date
    changed_date = l1.changed_date
    name = l1.name
    page = l1.page_link
    print(str(position) + " " + name)
    url = l1.url
    mailto = l1.mailto
    l1.delete()
    l2 = add_plugin(placeholder, 'LinkPlugin', language, position, parent,
                    name=name, external_link=url, mailto=mailto, internal_link=page)

    
def copy_one(texts, oldnew, l1):
    placeholder = l1.placeholder
    parent = l1.parent
    position = l1.position
    language = l1.language
    creation_date = l1.creation_date
    changed_date = l1.changed_date
    name = l1.name
    page_link = l1.page_link
    print(name)
    url = l1.url
    mailto = l1.mailto
    # la position n'a probablement aucune importance
    l2 = add_plugin(placeholder, 'LinkPlugin', language, 'last-child', parent,
                    name=name, external_link=url, mailto=mailto, internal_link=page_link)
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
def migrate_links():
    tilt = False
    a1 = L1.objects.all()
    tilt |= check_FilerLinkPlugin(a1)
    a2 = L2.objects.all()
    tilt |= check_Link(a2)
    assert(tilt == False)

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

    assert(len(lstrange) == 0)
    
    print("\nNow moving links in standard placeholders")
    for l1 in lnop:
        move_one(l1)

    print("\nNow moving creatins new links for texts")
    texts = set()
    oldnew = dict()
    for l1 in ltext:
        copy_one(texts, oldnew, l1)
    texts = list(texts)

    print("\nNow moving links in texts")
    for tt in texts:
        rename_plugins(oldnew, tt)

    print("\nNow removing oldlinks")
    for l1 in ltext:
        print(l1.id)
        l1.delete()

migrate_links()

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
