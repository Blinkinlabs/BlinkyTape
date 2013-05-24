jigFrameSize = 5;    // Extra material around edge of pcba (mm)
jigThickness = 5;    // Thickness of the jig (mm)
pogoPinDiameter = 1;        // Diameter of the pogo pin (mm)

module hole(x, y)
{
	translate([x,y,jigThickness/2])
		cylinder(r = pogoPinDiameter/2,
				jigThickness*1.1,
				center = true);
}

module jig(width, height)
{
	translate([-jigFrameSize,-jigFrameSize])
	    cube([width + 2*jigFrameSize,
			height + 2*jigFrameSize,
			jigThickness],
			center = false);
}

difference() {
	jig(20, 10);  // Put in the board dimensions here
	hole(3,1);    // Then add one of these for every hole
	hole(4,1);
	hole(5,1);
	hole(6,1);
	hole(3,5);
	hole(3,7);
}

