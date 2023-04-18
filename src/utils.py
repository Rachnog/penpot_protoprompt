import os
import xml.etree.ElementTree as ET

def run_svgoptim(input_fule_name, output_file_name):
    """
        Run svgo as a command line in Python
        For example ! svgo -i "../data/Bottom App Bar.svg" -o "../data/Bottom App Bar Opt.svg"
    """
    os.system(f"svgo -i {input_fule_name} -o {output_file_name}")

import xml.etree.ElementTree as ET

def remove_style(svg_file_path, output_file_path):
    # Parse the SVG file as an ElementTree object
    svg_root = ET.parse(svg_file_path).getroot()

    # Find the style element
    style_element = svg_root.find('.//{http://www.w3.org/2000/svg}style')

    # If the style element is found, remove its contents
    if style_element is not None:
        style_element.clear()

    # Remove namespace prefixes from tags
    for elem in svg_root.iter():
        elem.tag = elem.tag.split('}')[-1]

    # Serialize the modified ElementTree object to an SVG file
    with open(output_file_path, 'w') as f:
        f.write(ET.tostring(svg_root, encoding='unicode'))

