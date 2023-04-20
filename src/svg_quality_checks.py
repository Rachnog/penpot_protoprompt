from lxml import etree
import xml.etree.ElementTree as ET


def validate_svg(svg_string):
    try:
        etree.fromstring(svg_string)
    except:
        return False
    return True

def get_svg_size(svg_string):
    try:
        # Parse the SVG string as an ElementTree object
        svg_root = ET.fromstring(svg_string)
        # Get the 'width' and 'height' attributes from the root element
        width = svg_root.get('width')
        height = svg_root.get('height')
    except:
        width = -1
        height = -1
    finally:
        if width is None:
            width = -1
        if height is None:
            height = -1
    # Convert the strings to floats and return as a tuple
    return (float(width), float(height))


