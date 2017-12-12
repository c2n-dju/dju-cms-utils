# Cf. https://stackoverflow.com/questions/4888027/python-and-pip-list-all-versions-of-a-package-thats-available
for c in Django== \
Pillow== \
Unidecode== \
cmsplugin-filer== \
django-appconf== \
django-auth-ldap== \
django-classy-tags== \
django-cms== \
django-debug-toolbar== \
django-extensions== \
django-filer== \
django-formtools== \
django-mptt== \
django-polymorphic== \
django-reversion== \
django-sekizai== \
django-treebeard== \
djangocms-admin-style== \
djangocms-attributes-field== \
djangocms-file== \
djangocms-link== \
djangocms-page-sitemap== \
djangocms-picture== \
djangocms-snippet== \
djangocms-style== \
djangocms-text-ckeditor== \
djangocms-video== \
easy-thumbnails== \
html5lib== \
numpy== \
olefile== \
pipdeptree== \
psycopg2== \
python-ldap== \
six== \
sqlparse== ; do pip install $c ; done
