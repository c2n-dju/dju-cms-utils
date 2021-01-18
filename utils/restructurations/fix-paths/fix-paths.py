#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib.sites.models import Site
from django.urls import reverse

from cms.api import add_plugin

from cms.models.pagemodel          import Page
from cms.models.titlemodels        import Title


sites = Site.objects.get_queryset()

s = sites[0].id

root_drafts = Page.objects.drafts().on_site(s).filter(node__depth=1)

p = root_drafts[0]

n = p.node

n.is_root()

titles = Title.objects.filter(page=p) # les deux langues

t = titles[0]

assert(not(t.has_path_override))

t.path # 'trash'

n1= t.page.node









pa = Page.objects.get(id=9) # un objet
# Title.objects.get(page_id=9) # error, deux objets
Title.objects.filter(page_id=9) # deux objets un fr et un en
tfr = Title.objects.get(page_id=9, language='fr')
ten = Title.objects.get(page_id=9, language='en')
"""
tfr?
Title(id,
      language,
      title,
      page_title,
      menu_title,
      meta_description,
      slug,
      path,
      has_url_overwrite,
      redirect,
      page,
      creation_date,
      published,
      publisher_is_draft,
      publisher_public,
      publisher_state)
"""
# obsolète 
# tfr.page.path # u'laboratoire/services'
# ten.page.path # u'laboratoty/services'

# Les deux langues fr et en ont les mêmes placeholders
map(lambda x:x.id, tfr.page.placeholders.all())
map(lambda x:x.id, ten.page.placeholders.all())

# et mêmes plugins, ça cloche ?
map(lambda x:x.get_plugins_list(), tfr.page.placeholders.all())
map(lambda x:x.get_plugins_list(), ten.page.placeholders.all())

cfr = tfr.page.placeholders.get(slot='content')
cen = ten.page.placeholders.get(slot='content')

# 
page = tfr.page # ou ten.page
content = page.placeholders.get(slot='content')

sorted(map(lambda x:x.id, cfr.get_plugins())) == sorted(map(lambda x:x.id, content.get_plugins()))
plugs = content.get_plugins()
map(lambda x:x.language, plugs) # [u'fr', u'en', u'fr']
pfr1 = plugs[0]
pfr2 = plugs[2]
pen = plugs[1]

add_plugin(content, 'TextPlugin', 'en', 1, body="blabla 1")

enplugs = content.get_plugins(language='en')
tenplugs = enplugs.filter(plugin_type='TextPlugin')
map(lambda x:(x.id, x.djangocms_text_ckeditor_text.body[-100:]), tenplugs)
# ou mieux
map(lambda x:(x.id, x.get_bound_plugin().body[-100:]), tenplugs)

def en_text(placeholder):
    enplugs = content.get_plugins(language='en')
    plugs = enplugs.filter(plugin_type='TextPlugin')
    return map(lambda x:(x.id, x.djangocms_text_ckeditor_text.body[-100:]), plugs)


    
sp = StaticPlaceholder.objects.get(code='placo')
# Les placeholders
plapub = sp.public
pladra = sp.draft

plapub.get_plugins_list()
pladra.get_plugins_list()
plapub.page == None

#################
# On récapitule #
#################

"""
Page et placeholder ignorent les langues !

Une page (Page) est un nœud dans l'arborescence des pages.
Une page contient ensemble de placeholders (Placeholder).
Un placeholder est en géneral attribué à une page, jamais à deux,
mais il peut éventuellement ne pas avoir de page attribuée à un placeholder.
Par exemple s'il est référencé par un placeholder statique.

Un placeholder dans une page est identifié par son slot, typiquement "content".

Une page est reliée à N titres (Title), un par langue. Mais il peut manquer des titres.

Chaque placeholder contient une ensemble de plugins de différentes langues
placés à différentes positions.
Deux plugins de même langue ne peuvent pas partager la même position dans un placeholder.

Les placeholder statiques (StaticPlaceholder) ne sont pas reliés aux pages.
L'attribut creation_method ne semble pas servir à grand chose.
Dès qu'un template est lu avec une commande de static_template,
le placeholder statique ets créé ou s'il existe déjà se voir attribuer
creation_method = "template"


"""




"""





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
		print '"%s" id %d has "%s" placeholder slot which is no longer in use' % (
		    page.get_title(),
                    page.id,
		    placeholder.slot
		)

check_placeholders()


