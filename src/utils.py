import os
import xml.etree.ElementTree as ET

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
    drawing = svg2rlg(f'{svg_path}/{file_name}_optimized.svg')
    renderPM.drawToFile(drawing, f'{png_path}/{file_name}_optimized.png', fmt="PNG")
    return svg_short_opt

def load_raw_svg_optimize_clean(file_name, svg_path = '../data/svgs'):
    svg_short = open(f"{svg_path}/{file_name}.svg", "r").read()
    remove_style(f"{svg_path}/{file_name}.svg", f"{svg_path}/{file_name}_optimized.svg")
    run_svgoptim(f"{svg_path}/{file_name}_optimized.svg", f"{svg_path}/{file_name}_optimized.svg")
    svg_short_opt = open(f"{svg_path}/{file_name}_optimized.svg", "r").read()
    drawing = svg2rlg(f'{svg_path}/{file_name}_optimized.svg')
    return svg_short_opt

def load_css(file_name, css_path = '../data/css/incomplete'):
    csscontent = open(f"{css_path}/{file_name}.css", "r").read()
    return csscontent

def save_autocomplete_css(answer, filename, path = '../generated_data/css/'):
    with open(f"{path}/{filename}.css", "w") as f:
        f.write(answer)
    return answer

def compare_css(generated, original):
    ordered_generated = list(filter(None, sorted(generated.split("\n"))))
    ordered_original = list(filter(None, sorted(original.split("\n"))))
    print(ordered_generated)
    print(ordered_original)
    if ordered_generated == ordered_original:
        return True
    return False

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
