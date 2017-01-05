from __future__ import division

from solid import *
from solid.utils import *

META = {
    'model': 'ethernet',
    'author': 'Richard Marko',
    'date': '2017-01-04',
    'segments': 100,
}

# UTP cable holder generator
# inspired by http://www.thingiverse.com/thing:1320948/

x, y = 3, 3 # grid
#x, y = 4, 4 # grid
#x, y = 5, 4 # grid
#x, y = 11, 11 # grid

# use straight mount by default
use_cross_mount = not True

# holder hull params
h = 10. # holder height
corner_r=3. # holder corner radius
margin_y = 4. # y margin

# cable hole params
c_r = 2.8 # cable radius
d_x = 8. # cable hole x distance
d_y = 8. # cable hole y distance

# width of the gap between holes
gap_y = 3.5

# mount size
mount_x = 10.
mount_y = 4.
# mount hole size
mount_hole_y = 2.
mount_hole_z = 4.


#
# COMPUTED STUFF, don't change
#
# cable hole grid size
rx = (x - 1) * d_x
ry = (y - 1) * d_y

# rounded block size
rounded_x = rx + d_x
rounded_y = ry + d_y + margin_y

def rounded(x, y, h=2, r=1):
    corner = up(h/2)(cylinder(r=r, h=h, center=True))
    out = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            out.append(translate([i * (x/2. - r), j * (y/2. - r), 0])(corner))

    return hull()(out)

def mount_cross():
    o = cube([mount_x, mount_y, h], center=True)
    o -= translate([0, -mount_y/2. + mount_hole_y/2., 0])(
            cube([mount_x, mount_hole_y, mount_hole_z], center=True))
    return o

def hole():
    return cylinder(r=c_r, h=h*2, center=True)

def gap():
    return cube([d_x/2., gap_y, h*2], center=True)

def eth():
    o = translate([0, 0, -h/2.])(rounded(rounded_x, rounded_y, h=h, r=corner_r))

    for ix in range(x):
        for iy in range(y):
            o -= translate([ix * d_x - rx/2., iy * d_y - ry/2., 0])(hole())

    if x % 2 == 0:
        for side in [-1, 1]:
            for ix in range(int(x/2)):
                for yx in range(y):
                    o -= translate([(ix + 1) * d_x * side, yx * d_y - (-d_y/2. + y/2 * d_y), 0,])(gap())
    else:
        # generate zig-zag pattern
        for side in [-1, 1]:
            for ix in range(int((x+1)/2)):
                for yx in range(y):
                    ty = 0
                    off = 0
                    cross = 1
                    if side == 1:
                        off = 1
                        if yx % 2 == 0:
                            ty = cross
                    else:
                        if yx % 2 == 1:
                            ty = cross

                    o -= translate([(ix + ty + off) * d_x * side - (d_x/2.), yx * d_y - (-d_y/2. + y/2 * d_y), 0,])(gap())

    obj = mount_cross()
    if not use_cross_mount:
        obj = rotate([0, 90, 0])(obj)

    o += translate([0, mount_y/2. + rounded_y/2., 0])(obj)
    return o

if __name__ == "__main__":
    out = eth()
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False)
