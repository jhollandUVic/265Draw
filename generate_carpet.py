import sys
import math
import random
import re
import Line_Point_colour

'''
purpose
	write to stdout a Sierpinski Carpet in a 500 x 500 canvas
	with a number of recursion levels using a colour theme
preconditions
	recursion level is an integer between 0 and 4
	colour theme is one of: 'dark', 'light', 'medium'
reference
	See <http://lodev.org/cgtutor/sierpinski.html>
'''

cf_colour_names = 'css_colours.txt'
cl_recursion_range = [0, 4]
cl_canvas_bounds = [-250, 250, 250, -250]
cd_colour_themes = {'primary':'Red|Blue|Yellow',
					'secondary':'Orange|Purple|Green',
					'bold':'Dark|Deep',
					'tropical':'Pink|Teal|Turquoise|Purple|Fuchsia'
					}

'''
purpose
	write to stdout a set of coloured lines making up a square in
	a Sierpinksi Carpet
preconditions
	x1, y1, x2, y2 are the four points of the square
	colour is a valid colour name
'''
def draw_square(x1, y1, x2, y2, colour):
	# Draw boundaries of square
	point0 = Line_Point_colour.Point(x1, y1)
	point1 = Line_Point_colour.Point(x2,y1)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	point0 = Line_Point_colour.Point(x2,y1)
	point1 = Line_Point_colour.Point(x2, y2)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	point0 = Line_Point_colour.Point(x2, y2)
	point1 = Line_Point_colour.Point(x1, y2)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	point0 = Line_Point_colour.Point(x1, y2)
	point1 = Line_Point_colour.Point(x1, y1)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	# Draw diagonal cross on square
	point0 = Line_Point_colour.Point(x1, y2)
	point1 = Line_Point_colour.Point(x2, y1)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	point0 = Line_Point_colour.Point(x1, y1)
	point1 = Line_Point_colour.Point(x2, y2)
	line = Line_Point_colour.Line(point0, point1, colour)
	print 'line', line
	
'''
purpose
	Build a Sierpinksi Carpet at the current recursion level
	then ask for eight more carpets at the next recursion level
preconditions
	this_step is a recursion level
	x1, y1, x2, y2 are the four points of the square
	colour and prev_colour are valid colour names
'''
def draw_carpet(this_step, x1, y1, x2, y2, colour, prev_colour):
	# Build new square one ninth the size in center of given coordinates
	r_x1 = (2 * x1 + x2)/3.0
	r_y1 = (2 * y1 + y2)/3.0
	r_x2 = (x1 + 2 * x2)/3.0
	r_y2 = (y1 + 2 * y2)/3.0
	draw_square(r_x1, r_y1, r_x2, r_y2, colour)
	
	# Call draw_carpet another 8 times, once for each of the squares
	# around the one that was just drawn.
	if this_step > 0:
		next_step = this_step - 1
		# Choose a colour not recently used
		while True:
			random.shuffle(l_colours)
			next_colour = l_colours[0]
			if next_colour != colour and next_colour != prev_colour:
				break
				
		draw_carpet(next_step, r_x1,   y1, r_x2, r_y1, next_colour, colour) # top center
		draw_carpet(next_step,   x1,   y1, r_x1, r_y1, next_colour, colour) # top left
		draw_carpet(next_step,   x1, r_y1, r_x1, r_y2, next_colour, colour) # center left
		draw_carpet(next_step,   x1, r_y2, r_x1,   y2, next_colour, colour) # bottom left
		draw_carpet(next_step, r_x1, r_y2, r_x2,   y2, next_colour, colour) # bottom center
		draw_carpet(next_step, r_x2, r_y2,   x2,   y2, next_colour, colour) # bottom right
		draw_carpet(next_step, r_x2, r_y1,   x2, r_y2, next_colour, colour) # center right
		draw_carpet(next_step, r_x2,   y1,   x2, r_y1, next_colour, colour) # top right

'''
purpose
	convert the lines in stdin to a list containing, for each line,
	a valid css colour name.
preconditions
	file_object is a reference to a readable file containing legal 
	colour names ('css.colours.txt')
'''
def load_line_file(file_object):

	# Monochrome colours or colours with not enough contrast
	# to show well on a white background
	unwanted_colours = ['White', 'Light', 'Grey', 'Gray', 'Black',
						'Gainsboro', 'Ivory', 'Snow']
						
	line_objects = [ ]
	for line in file_object:
		if line[-2:] == '\r\n': # Windows
			line = line[:-2] # strip carriage return and newline
		elif line[-1] == '\n': # Linux
			line = line[:-1] # strip newline
		line_object = line
		
		# Remove colours which fade into a white background
		# or which are monochrome colours
		if not any(unwanted_colour in line_object
					for unwanted_colour in unwanted_colours):
			line_objects.append(line_object)

	return line_objects

# ********** process the command line arguments
if len(sys.argv) != 3:
	print >> sys.stderr, 'Syntax: ' + sys.argv[0] + ' Supply recursion steps and colour theme'
	sys.exit(2)
try:
	recursion_steps = int(sys.argv[1])
except ValueError:
	print >> sys.stderr, 'Value Error: ' + sys.argv[0] + ' Supply recursion steps as integer'
	sys.exit(3)
if not ( cl_recursion_range[0] <= recursion_steps <= cl_recursion_range[1] ):
	print >> sys.stderr, 'Values: ' + sys.argv[0] + ' Recursion steps out of range ' \
			+ str(cl_recursion_range[0]) + ' to ' + str(cl_recursion_range[1])
	sys.exit(4)

try:
	colour_theme = str(sys.argv[2])
except ValueError:
	print >> sys.stderr, 'Value Error: ' + sys.argv[0] + ' Supply colour theme as string'
	sys.exit(5)

if colour_theme not in cd_colour_themes:
	print >> sys.stderr, 'Values: ' + sys.argv[0] + ' Supply colour theme from:',
	print >> sys.stderr, ", ".join(map(str, cd_colour_themes))
	sys.exit(6)

# Load valid css colours into list
fh_css_colour_names = open(cf_colour_names, 'r')
l_colour_names = load_line_file(fh_css_colour_names)
fh_css_colour_names.close

theme_pattern = cd_colour_themes[colour_theme]
	
# Build a random list of colours chosen according to theme specified
l_colours = filter(lambda x: re.search(theme_pattern, x), l_colour_names)
random.shuffle(l_colours)

# Select two different colour names so succeeding levels are different colours
this_colour = l_colours[0]
prev_colour = l_colours[1]

# Co-ordinates describe a square, upper left to bottom right.
draw_carpet(recursion_steps, cl_canvas_bounds[0], cl_canvas_bounds[1],
			cl_canvas_bounds[2], cl_canvas_bounds[3], this_colour, prev_colour)

