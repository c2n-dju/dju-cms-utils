#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib.sites.models import Site

from cms.models.pagemodel          import Page
# from cms.models.titlemodels        import Title

sites = Site.objects.get_queryset()

for site in sites:
    s = site.id
    print("\n", s, " ", site.name)
    root_drafts = Page.objects.drafts().on_site(s).filter(node__depth=1)
    for p in root_drafts:
        for language in p.get_languages():
            print(p.get_title(language))
            p._update_title_path_recursive(language)
