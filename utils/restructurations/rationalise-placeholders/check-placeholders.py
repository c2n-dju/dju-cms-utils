#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, django
sys.path.append(os.environ["DJU_DIR"]) #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dju.settings")
django.setup()


from cms.models.pluginmodel import CMSPlugin
from cms.models.placeholdermodel import Placeholder
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


from django.template import TemplateDoesNotExist
from cms.utils.placeholder import get_placeholders


"""
[u'actu_labo',
 u'clipboard',
 u'content',
 u'descriptif',
 u'descriptif_departement',
 u'equipes',
 u'info',
 u'info2',
 u'info_departement',
 u'la_centrale',
 u'labo',
 u'plateforme',
 u'semin_labo',
 u'service',
 u'services',
 u'uv']
"""

# https://gist.github.com/nicksnell/9228580 modifié ATTENTION BUG Manque map slot dans template_placeholders

def get_used_templates():
    templates = set()
    for page in sorted(Page.objects.all(), key=lambda x:x.get_title()):
        templates.add(page.get_template())
    return sorted(templates)


def check_placeholders(dt, dp):
    # Go though each page, look at the placeholders in the page
    # template and compare to what it currently has.
    for page in sorted(Page.objects.all(), key=lambda x:x.get_title()):
        try:
            template = page.get_template()
            # list() is needed with Python3, why? Cf. https://www.quora.com/unanswered/Why-map-content-is-vanishing-outside-of-a-try-with-Python3
            template_placeholders = list(map(lambda x:x.slot, get_placeholders(template)))
        except TemplateDoesNotExist:
            print('** "%s" has template "%s" which could not be found **' % (
                page.get_title(),
                page.template,
            ))
            continue
        for language in ['fr', 'en']:
            papa = page.site.name + ':' + page.get_absolute_url(language=language)
            if not page.is_published(language):
                papa += ' (unpublished)'
            papa += ' ' + str(page.id)
            for placeholder in template_placeholders:
                dp[placeholder].add(papa)
            dt[template].add(papa)
           
        for placeholder in page.placeholders.all():
            if not placeholder.slot in template_placeholders:
                for language in ["fr", "en"]:
                    plugs = placeholder.get_plugins(language=language)
                    if len(plugs) > 0:
                        print('"%s" id %d has "%s" placeholder slot with not in %s' % (
                            page.get_absolute_url(language=language),
                            page.id,
                            placeholder.slot,
                            list(template_placeholders)
                        ))


ps = sorted(set(map(lambda x:x.slot, Placeholder.objects.all())))
print("\nPlaceholders:")
print(ps)

dp = dict()
for p in ps:
    dp[p] = set()


print("\nUsed templates:")
ts = get_used_templates()
print(ts)

dt = dict()
for t in ts:
    dt[t] = set()


print("\nAnomalies:")
check_placeholders(dt, dp)

print("\nTemplates:")
for t in sorted(dt.keys()):
    print()
    print(t)
    print('\n'.join(sorted(dt[t])))

print("\nPlaceholders:")
for p in sorted(dp.keys()):
    print()
    print(p)
    if (p == "content"):
        print("List omitted,", len(dp[p]), "elements")
    else:
        print('\n'.join(sorted(dp[p])))

