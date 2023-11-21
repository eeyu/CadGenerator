// Begin.
union() {
union() {
union() {
difference() {
union() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}

union() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}
}

intersection() {
difference() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}
}

difference() {
union() {
difference() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}

intersection() {
rotate([0, -0, 0])
translate([0, 0, 0])
cube(size = [10, 10, 10], center = true);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}
}

intersection() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

rotate([0, -0, 0])
translate([0, 0, 12])
cube(size = [38, 10, 14], center = true);
}
}
}

difference() {
translate([0, 0, 0])
sphere(r = 57, $fn = 12);

translate([0, 0, 0])
sphere(r = 57, $fn = 12);
}
}
// End.