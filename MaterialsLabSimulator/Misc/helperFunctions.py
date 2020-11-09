'''
Description: This file contains random functions that are used in multiple places
Author: Andrew Lucentini
'''
def from_rgb(rgb):
    """
    Translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

def scaleCoordinates(x0, y0, x1, y1, scaleX, scaleY):
	"""
	Return scaled coordinates given original coordinates and scale factor (as a percentage). Object must
	be contained in box
	"""
	if x1 >= x0:
		width = x1-x0
		xCenter = width/2 + x0
		newWidth = scaleX*width
		n_x0 = xCenter-newWidth/2
		n_x1 = xCenter+newWidth/2
	else:
		width = x0-x1
		xCenter = width/2 + x1
		newWidth = scaleX*width
		n_x0 = xCenter+newWidth/2
		n_x1 = xCenter-newWidth/2
	if y1 >= y0:
		length = y1-y0
		yCenter = length/2 + y0
		newLength = scaleY*length
		n_y0 = yCenter-newLength/2
		n_y1 = yCenter+newLength/2
	else:
		length = y0-y1
		yCenter = length/2 + y1
		newLength = scaleY*length
		n_y0 = yCenter+newLength/2
		n_y1 = yCenter-newLength/2
	
	return n_x0, n_y0, n_x1, n_y1

def stretchCoordinates(x0, y0, x1, y1, pixX, pixY):
	"""
	Return stretched coordinates given original coordinates and factor (as num of pixels)
	"""
	if x1 >= x0:
		x0 -= pixX
		x1 += pixX
	else:
		x0 += pixX
		x1 -= pixX
	if y1 >= y0:
		y0 -= pixY
		y1 += pixY
	else:
		y0 += pixY
		y1 -= pixY

	return x0, y0, x1, y1

def translateCoordinates(x0, y0, x1, y1, pixX, pixY):
	"""
	Translate coordinates by number of pixels
	"""
	return x0+pixX, y0+pixY, x1+pixX, y1+pixY

def multiple(*func_list):
	"""
	Run multiple functions as one
	"""
	return lambda *args, **kw: [func(*args, **kw) for func in func_list]; None
