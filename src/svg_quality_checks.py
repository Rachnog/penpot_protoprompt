from lxml import etree
import xml.etree.ElementTree as ET


def validate_svg(svg_string):
    try:
        etree.fromstring(svg_string)
    except:
        return False
    return True

def get_svg_size(svg_string):
    # Parse the SVG string as an ElementTree object
    svg_root = ET.fromstring(svg_string)
    
    # Get the 'width' and 'height' attributes from the root element
    width = svg_root.get('width') or 0
    height = svg_root.get('height') or 0
    
    # Convert the strings to floats and return as a tuple
    return (float(width), float(height))


