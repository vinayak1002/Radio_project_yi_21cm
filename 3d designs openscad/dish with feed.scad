// ##################################################################
// ##     V4 Radio Telescope Assembly (Corrected Rim Mount)      ##
// ##################################################################

// Part 1: Parameters & Calculations
// ===================================
// -- Dish Parameters
dish_diameter = 2450; 
dish_sagitta = 13.5 * 25.4; // 13.5 inches

// -- Feed Parameters
feed_waveguide_diameter = 115; // Please confirm this measurement
feed_choke_diameter = 210; 
feed_waveguide_height = 105;
feed_choke_height = 105;

// -- Support Arm Parameters (Easy to change here)
arm_count = 4;
pipe_diameter = 30; // << CHANGE PIPE DIAMETER HERE (e.g., to 25 or 40)

// -- Calculated Values
dish_radius = dish_diameter / 2;
choke_radius = feed_choke_diameter / 2;
focal_length = pow(dish_diameter, 2) / (16 * dish_sagitta);


// -- Echo results to the console
echo("--- Design Values ---");
echo(str("Focal Length (mm): ", focal_length));
echo(str("f/D Ratio: ", focal_length / dish_diameter));
echo("---------------------");


// Part 2: Modules for Each Component
// ====================================

module parabolic_dish() {
    rotate_extrude(convexity = 10) {
        polygon(points=[
            for(x=[0:dish_radius/100:dish_radius]) 
                [x, (pow(x,2) / (4*focal_length))]
        ]);
    }
}

module kumar_feed() {
    union() {
        translate([0, 0, feed_choke_height / 2])
            cylinder(h = feed_choke_height, d = feed_choke_diameter, center=true);
        translate([0, 0, feed_choke_height + (feed_waveguide_height / 2)])
            cylinder(h = feed_waveguide_height, d = feed_waveguide_diameter, center=true);
    }
}

module support_structure() {
    for (i = [0 : arm_count - 1]) {
        angle = i * (360 / arm_count);
        
        // ** THE FIX IS HERE **
        // The start point's Z-value is now set to dish_sagitta
        start_point = [
            dish_radius * cos(angle), 
            dish_radius * sin(angle), 
            dish_sagitta // <-- This ensures the pipe starts on the rim
        ];
        
        end_point = [
            choke_radius * cos(angle), 
            choke_radius * sin(angle), 
            focal_length
        ];
        
        color("DarkSlateGray") 
        hull() {
            translate(start_point) 
                sphere(d=pipe_diameter);
            translate(end_point) 
                sphere(d=pipe_diameter);
        }
    }
}


// Part 3: Final Assembly
// ========================

color("silver")
    parabolic_dish();
    
support_structure();
    
color("LightSteelBlue")
    translate([0, 0, focal_length])
        kumar_feed();