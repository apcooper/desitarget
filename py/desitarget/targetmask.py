from desiutil.bitmask import BitMask

import os
import sys
import yaml
from pkg_resources import resource_filename
#- Load bit definitions from yaml file
_filepath = resource_filename('desitarget', "data/targetmask.yaml") 
with open(_filepath) as fx:
    _bitdefs = yaml.load(fx)

#- priorities are defined in the yaml file, but they aren't a bitmask
#- and they require some extra processing
for maskname, priorities in _bitdefs['priorities'].items():
    for bitname in priorities:
        #- "SAME_AS_XXX" enables one bit to inherit priorities from another
        if isinstance(priorities[bitname], str) and \
            priorities[bitname].startswith('SAME_AS_'):
                other = priorities[bitname][8:]
                priorities[bitname] = priorities[other]

        #- fill in default "more" priority to be same as "unobs"
        if isinstance(priorities[bitname], dict):
            if 'MORE_ZWARN' not in priorities[bitname]:
                priorities[bitname]['MORE_ZWARN'] = priorities[bitname]['UNOBS']
            if 'MORE_ZGOOD' not in priorities[bitname]:
                priorities[bitname]['MORE_ZGOOD'] = priorities[bitname]['UNOBS']

            #- fill in other states as 0 priority
            for state, blat, foo in _bitdefs['obsmask']:
                if state not in priorities[bitname]:
                    priorities[bitname][state] = 0
        else:
            priorities[bitname] = dict()


    #- add to the extra info dictionary for this target mask
    for bitdef in _bitdefs[maskname]:
        bitname = bitdef[0]
        bitdef[3]['priorities'] = priorities[bitname]

#- convert to BitMask objects
desi_mask = BitMask('desi_mask', _bitdefs)
mws_mask = BitMask('mws_mask', _bitdefs)
bgs_mask = BitMask('bgs_mask', _bitdefs)
obsconditions = BitMask('obsconditions', _bitdefs)
obsmask = BitMask('obsmask', _bitdefs)

#-------------------------------------------------------------------------
#- Do some error checking that the bitmasks are consistent with each other
# error = False
# for mask in desi_target, mws_target, bgs_target:
#     for bitname in targetmask.names:
#         if targetmask[bitname]
#     if bitname not in priorities.keys():
#         print >> sys.stderr, "ERROR: no priority defined for "+bitname
#         error = True
#
# for bitname in priorities.keys():
#     if bitname not in targetmask.names():
#         print >> sys.stderr, "ERROR: priority defined for bogus name "+bitname
#         error = True
#
# if error:
#     raise ValueError("mismatch between priority and targetmask definitions")
