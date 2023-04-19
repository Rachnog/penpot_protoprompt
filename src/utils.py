import os
import xml.etree.ElementTree as ET
import re

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM, renderPDF

def run_svgoptim(input_fule_name, output_file_name):
    """
        Run svgo as a command line in Python
        For example ! svgo -i "../data/Bottom App Bar.svg" -o "../data/Bottom App Bar Opt.svg"
    """
    os.system(f"svgo -i {input_fule_name} -o {output_file_name}")


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


def load_raw_svg_optimize_clean_save_png(file_name, svg_path = '../data/svgs', png_path = '../data/pngs'):
    remove_style(f"{svg_path}/{file_name}.svg", f"{svg_path}/{file_name}_optimized.svg")
    run_svgoptim(f"{svg_path}/{file_name}_optimized.svg", f"{svg_path}/{file_name}_optimized.svg")
    svg_short_opt = open(f"{svg_path}/{file_name}_optimized.svg", "r").read()
    # svg_short_opt = shorten_svg_ids(svg_short_opt)
    # svg_short_opt = round_svg_numbers(svg_short_opt)
    drawing = svg2rlg(f'{svg_path}/{file_name}_optimized.svg')
    renderPM.drawToFile(drawing, f'{png_path}/{file_name}_optimized.png', fmt="PNG")
    return svg_short_opt

def load_raw_svg_optimize_clean(file_name, svg_path = '../data/svgs'):
    remove_style(f"{svg_path}/{file_name}.svg", f"{svg_path}/{file_name}_optimized.svg")
    run_svgoptim(f"{svg_path}/{file_name}_optimized.svg", f"{svg_path}/{file_name}_optimized.svg")
    svg_short_opt = open(f"{svg_path}/{file_name}_optimized.svg", "r").read()
    # svg_short_opt = shorten_svg_ids(svg_short_opt)
    # svg_short_opt = round_svg_numbers(svg_short_opt)
    return svg_short_opt


def save_gpt_answer_as_svg_and_png(answer, filename, path = '../generated_data/'):
    with open(f"{path}/{filename}.svg", "w") as f:
        f.write(answer)
    svg_short_opt = load_raw_svg_optimize_clean_save_png(filename, svg_path = path, png_path = path)
    return svg_short_opt

def save_gpt_answer_as_svg(answer, filename, path = '../generated_data/'):
    with open(f"{path}/{filename}.svg", "w") as f:
        f.write(answer)
    svg_short_opt = load_raw_svg_optimize_clean(filename, svg_path = path)
    return svg_short_opt


def shorten_svg_ids(svg_string, prefix='s'):
    """
    Shortens the id properties in an SVG string by replacing them with a
    prefix and a numeric index. Returns the modified SVG string.
    
    Args:
        svg_string (str): An SVG string with long id properties.
        prefix (str): A prefix to use for the new id properties.
        
    Returns:
        str: The modified SVG string with shortened id properties.
    """
    id_pattern = re.compile(r'id="([^"]+)"')
    new_ids = {}
    index = 1
    
    def replace_id(match):
        old_id = match.group(1)
        if old_id in new_ids:
            return f'id="{new_ids[old_id]}"'
        else:
            nonlocal index
            new_id = f'{prefix}{index}'
            new_ids[old_id] = new_id
            index += 1
            return f'id="{new_id}"'
    
    return id_pattern.sub(replace_id, svg_string)


def round_svg_numbers(svg_string):
    """
    Rounds all the numbers in an SVG string to 2 decimal places. Returns
    the modified SVG string.
    
    Args:
        svg_string (str): An SVG string with numbers to round.
        
    Returns:
        str: The modified SVG string with rounded numbers.
    """
    number_pattern = re.compile(r'[0-9]+\.[0-9]+|[0-9]+')
    
    def round_number(match):
        return f'{float(match.group(0)):.2f}'
    
    return number_pattern.sub(round_number, svg_string)
