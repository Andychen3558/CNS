#!/usr/bin/env python3

from coll import Collider, md5pad, filter_disallow_binstrings
import os
import base64

# We generate a file of the form:
"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

diff = '''<one of 2 collision blocks>'''
same = '''<first of the 2 collision blocks>'''

if (same == diff):
    print "good"

else:
    print "evil"
"""


collider = Collider(blockfilter=filter_disallow_binstrings([b'\0', b"'''"]))

prefix1 = b"""#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#"""
prefix2 = b"""\ndiff = '''"""

# Ensure prefix is a multiple of 64 bytes
prefix = prefix1 + md5pad(prefix1 + prefix2, b' ') + prefix2

# Load the first half of the collision files that opens the 'diff' variable delcaration
collider.bincat(prefix)
# Fill in the 'diff' variable with 2 different blocks that may be chosen
collider.safe_diverge()

postfix = b"""'''
same = '''"""

c1, c2 = collider.get_last_coll()

postfix += c1

postfix += b"""'''

if (same == diff):
    import glob
    print glob.glob('home/md5/*')

else:
    f = open('home/md5/b0nU5_FL4g_Y0U_F0unD_m3')
    print f.readline()
    
"""

# Close the 'diff' variable string and declare the 'same' variable to always have the 1st collision block
# Thus for one file: same == diff, but for the other: same != diff
collider.bincat(postfix)

# Write out the good and evil scripts
cols = collider.get_collisions()

print(str(base64.b64encode(next(cols)))[2:-1])
print(str(base64.b64encode(next(cols)))[2:-1])
