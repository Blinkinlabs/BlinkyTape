LED_size = 5;
LED_spacing = 50/3;
frame_size = 200;
padding = (frame_size - (LED_spacing * 7))/2;
cap_hole_h = 4.25;
cap_hole_w = 11;
side_mat_thickness = 3.2; // 1/8"

tab_length = 75;
tab_offset = (frame_size - tab_length)/2;

inner_frame_size = 200 - (6*side_mat_thickness);
inner_padding = (inner_frame_size - (LED_spacing * 7))/2;
inner_offset = (padding - inner_padding);

side_thickness = 17;

module hole(x,y) {
  translate([
    x * LED_spacing,
    y * LED_spacing])
  {
      square(LED_size);
      translate([
        (cap_hole_w - LED_size) / -2,
        (LED_size - cap_hole_h) / 2])
        square([cap_hole_w,cap_hole_h]);
  }
}

module LED_holes() {
  for( i = [1 : 6] , j = [0 : 7] )
	hole(j,i);
  for( j = [1 : 6] ) {
    hole(j, 0);
    hole(j, 7);
  }
}

module usb_space() {
  translate([
	-padding*0.4,
	7*LED_spacing+padding*0.65
  ]) {
	  square([67,15]);
	  for( x = [10, 25], y = [-7, 19] )
	    translate([x,y]) square([5,3]);
  }
}

module mount_mount_holes() {
  for( x = [20, inner_frame_size-20],
       y = [25, inner_frame_size-25] )
	translate([x,y]) circle(1.5, center=true);
}

// the layer that actually holds the LEDs
module LED_mount() {
  translate([inner_offset,inner_offset]){
	  difference() {
	    square(inner_frame_size);
	    translate([inner_padding,inner_padding]) LED_holes();
		usb_space();
		mount_mount_holes();
	  }
   }
}

module LED_frame_back() {
  difference(){
    square(frame_size);
	translate([inner_offset, inner_offset])
	{
		mount_mount_holes();
	}
	for(y = [0, frame_size - side_mat_thickness])
	{
		translate([tab_offset,y])
			square([tab_length, side_mat_thickness + 0.1]);
	}
	for(x = [0, frame_size - side_mat_thickness])
	{
		translate([x, tab_offset])
			square([side_mat_thickness +0.1, tab_length]);
	}
  }
}

module frame_left(){
	difference(){
		square([side_thickness, frame_size - side_mat_thickness]);
		for(y = [0, tab_offset+tab_length-0.1]){
			translate([0,y])	square([side_mat_thickness, tab_offset+0.1]);
		}
		translate([side_mat_thickness,tab_offset + tab_length + (tab_offset*0.33)]){
			square(6);
		}
	}
}

module frame_right(){
	difference(){
		square([side_thickness, frame_size - side_mat_thickness]);
		for(y = [0, tab_offset+tab_length-0.1]){
			translate([0,y])	square([side_mat_thickness, tab_offset+0.1]);
		}
	}
}

module frame_bottom(){
	translate([side_mat_thickness,0]) {
		difference(){
			square([frame_size - (2*side_mat_thickness), side_thickness]);
			square([tab_offset-side_mat_thickness+0.1, side_mat_thickness]);
			translate([tab_offset+tab_length-side_mat_thickness-0.1,0])
				square([tab_offset+0.1, side_mat_thickness]);
		}
	}
}

module frame_top(){
	difference(){
		square([frame_size, side_thickness]);
		square([tab_offset+0.1, side_mat_thickness]);
		translate([tab_offset+tab_length-0.1,0])
			square([tab_offset+0.1, side_mat_thickness]);
	}
}

module LED_frame_front() {
	square(frame_size);
}

//LED_mount();
//LED_frame_back();
//frame_left();
//frame_right();
//frame_top();
//frame_bottom();
//LED_frame_front();