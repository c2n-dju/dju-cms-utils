#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from cms.models.placeholdermodel import Placeholder
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title

from django.template import TemplateDoesNotExist
from cms.utils.placeholder import get_placeholders

a = Placeholder.objects.all()
print (sorted(set(map(lambda x:x.slot, a))))

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

def check_placeholders():
    # Go though each page, look at the placeholders in the page
    # template and compare to what it currently has.
    for page in sorted(Page.objects.all(), key=lambda x:x.get_title()):
	try:
	    template_placeholders = map(lambda x:x.slot, get_placeholders(page.get_template()))
	except TemplateDoesNotExist:
	    print '** "%s" has template "%s" which could not be found **' % (
		page.get_title(),
		page.template,
	    )
	    continue
	for placeholder in page.placeholders.all():
	    if not placeholder.slot in template_placeholders:
                for language in ["fr", "en"]:
                    plugs = placeholder.get_plugins(language=language)
                    if len(plugs) > 0:
		        print '"%s" id %d has "%s" placeholder slot with not in use data' % (
		            page.get_absolute_url(language=language),
                            page.id,
		            placeholder.slot
		        )

check_placeholders()
