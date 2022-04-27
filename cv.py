from fpdf import FPDF
from datetime import datetime
import os

class FontNotTTFError(Exception): pass

def add_ttf(font: str) -> str:

    if not font.endswith('.ttf'):
        if '.' in font:
            raise FontNotTTFError
        else:
            font = font + '.ttf'
    return font

def find_font(font: str, paths: list[str]=[]) -> str:

    font = add_ttf(font)
    if not paths:
        HOME: str = os.environ['HOME']
        paths = [ 
                HOME + '/.local/share/fonts/', 
                HOME + '/.fonts',
                '/usr/share/fonts/TTF/' ]
    
    for path in paths:
        for _, _, fonts in os.walk(path):
            if font in fonts:
                return path + font
    raise LookupError('Font not found. please specify a existing font')

def top_bar(font: str):

    methods = [
            'set_margin(0)',
            'add_font(font, fname=find_font(font))',
            'set_font(font, size=16)',
            'set_fill_color(26, 28, 29)',
            'set_text_color(255, 255, 255)',
            'cell(w=0, h=8, align=\'R\',fill=True, txt=' + \
            f"'{chr(0x1F5D3)} {datetime.today().strftime('%b %Y')}  ')",
            'ln(h=24.0)',
            ]
    for method in methods:
        eval(f'pdf.{method}')

# Left Column
#pdf.set_font('courier', size=24)
#pdf.set_text_color(0)
#pdf.set_margin(12)
#pdf.cell(txt='Hello World')

if __name__ == '__main__':

    pdf = FPDF()
    pdf.add_page()
    top_bar('Symbola')

    pdf.output('cv.pdf')

