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
    svg_short = open(f"{svg_path}/{file_name}.svg", "r").read()
    remove_style(f"{svg_path}/{file_name}.svg", f"{svg_path}/{file_name}_optimized.svg")
    run_svgoptim(f"{svg_path}/{file_name}_optimized.svg", f"{svg_path}/{file_name}_optimized.svg")
    svg_short_opt = open(f"{svg_path}/{file_name}_optimized.svg", "r").read()
    svg_short_opt = round_svg_numbers(svg_short_opt)
    drawing = svg2rlg(f'{svg_path}/{file_name}_optimized.svg')
    renderPM.drawToFile(drawing, f'{png_path}/{file_name}_optimized.png', fmt="PNG")
    return svg_short_opt


def save_gpt_answer_as_svg_and_png(answer, filename, path = '../generated_data/'):
    with open(f"{path}/{filename}.svg", "w") as f:
        f.write(answer)
    svg_short_opt = load_raw_svg_optimize_clean_save_png(filename, svg_path = path, png_path = path)
    return svg_short_opt


def round_svg_numbers(svg_string):
    # Round all numbers to a float with two decimal points
    def round_number(match):
        return '{:.2f}'.format(float(match.group(0)))
    # Use regular expressions to find all numbers in the SVG string and round them
    svg_string = re.sub(r'\d+\.\d+', round_number, svg_string)
    return svg_string