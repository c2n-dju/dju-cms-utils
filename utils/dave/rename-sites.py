#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import sys
import getpass

sys.path.append(os.environ['DJU_DIR'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dju.settings")

import django
django.setup()

from django.contrib.sites.models import Site

sites = {
    1: 'www',
    6: 'minao',
    7: 'cimphonie',
    8: 'crime',
    9: 'experfo',
    10: 'biosys',
    11: 'comics',
    12: 'dynanets',
    13: 'elphyse',
    14: 'ephycas',
    15: 'epla',
    16: 'goss',
    17: 'instrum',
    18: 'mat2d',
    19: 'mimed',
    20: 'minaphot',
    21: 'mnoems',
    22: 'integnano',
    23: 'toniq',
    24: 'nanophotonit',
    25: 'piment',
    26: 'nomade',
    27: 'oxide',
    28: 'phodev',
    29: 'phynano',
    30: 'qcl',
    31: 'qd',
    32: 'poem',
    33: 'panam',
    34: 'heterna',
    35: 'sunlit',
    36: 'odin',
    37: 'test01',
    38: 'test02',
    39: 'test03',
    40: 'qpc',
}


# code bricolé !
lasti = sorted(sites.keys())[-1]
print('--- NOW renaming until ' + str(lasti))
user = getpass.getuser()
if user != 'davecms':
    print('You are not davecms, you are ' + user)
    exit() 
if platform.node() != "webc2n1.c2n.u-psud.fr":
    print('platform.node() != "webc2n1.c2n.u-psud.fr"')
    exit()
for site in [1] + list(range(6,lasti+1)):
    s = Site.objects.get(id=site)
    if s.domain != 'edith-' + sites[site] + '.c2n.universite-paris-saclay.fr':
        print(s.domain + ' != edith-' + sites[site] + '.c2n.universite-paris-saclay.fr')
        continue 
    s.domain = 'test-' + sites[site] + '.c2n.science'
    print(s.domain)
    s.save()
