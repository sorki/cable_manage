from __future__ import division

from solid import *
from solid.utils import *

META = {
    'model': 'simple',
    'author': 'Richard Marko',
    'date': '2016-02-16',
    'segments': 100,
}



def simple(x=15, y=10, z=10):
    w = 3
    gap = 4
    o = cube([x, y, z], center=True)
    o -= cube([x - w, y + 10, z - w], center=True)
    o -= up(w)(cube([gap, y + 10, z], center=True))
    o -= debug(down(z)(cylinder(r=1.8, h=z)))
    return o

if __name__ == "__main__":
    out = rotate([90, 0, 0])(simple())
    out = rotate([90, 0, 0])(simple(z=20))

    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False)
