from fpdf import FPDF, XPos, YPos
from datetime import datetime
import os

class FontNotTTFError(Exception): pass

class CurriculumVitae(FPDF):

    def __init__(self, font: str, calemoji: str='') -> None:
        super().__init__()
        self.h_font: str = self._ttf(font)
        self.calemoji: str = chr(0x1F5D3) if not calemoji else calemoji
        self.date: str = datetime.today().strftime('%b %Y')
        self.h_text: str = f"'{self.calemoji} {self.date}  ')"

    def _ttf(self, font) -> str:
    
        if not font.endswith('.ttf'):
            if '.' in font: raise FontNotTTFError
            else: font = font + '.ttf'
        return font

    def _font_path(self, paths: list[str]=[]) -> str:
    
        if not paths:
            HOME: str = os.environ['HOME']
            paths = [ 
                    HOME + '/.local/share/fonts/', 
                    HOME + '/.fonts',
                    '/usr/share/fonts/TTF/' 
                    ]
        
        for path in paths:
            for _, _, fonts in os.walk(path):
                if self.h_font in fonts:
                    return path + self.h_font
        raise LookupError('Font not found. Please specify an existing font')

    def header(self):
    
        methods = [
                'set_margin(0)',
                'add_font(self.h_font, fname=self._font_path())',
                'set_font(family=self.h_font, size=16)',
                'set_fill_color(26, 28, 29)',
                'set_text_color(255, 255, 255)',
                'cell(w=0, h=8, align=\'R\',fill=True, txt=' + self.h_text,
                ]
        for method in methods:
            eval(f'self.{method}')


if __name__ == '__main__':


    pdf = CurriculumVitae('Symbola')
    pdf.add_page()
    #top_bar('Symbola')
    # Left Column
    pdf.set_font(family='Courier', size=12)
    pdf.set_text_color(0)
    pdf.set_margin(12)
    with open('curri-br') as fh:
        txt = fh.read()
    pdf.set_left_margin(20)
    pdf.set_y(30)
    pdf.multi_cell(w=100, align='L', txt=txt, markdown=True)
    pdf.ln(20)

    pdf.set_left_margin(140)
    pdf.set_y(-180)
    #pdf.set_y = -200

    with open('contact-skills') as fh:
        txt = fh.read()
    pdf.multi_cell(w=50, align='L', txt=txt, markdown=True)
    pdf.ln(20)

    pdf.output('cv.pdf')

