#!/usr/bin/env python
'''
    File name: cv.py
    Author: Diêgo Duarte
    Date created: 2022/04/26
    Python Version: 3.10.4
'''

from fpdf import FPDF
from datetime import datetime
from sys import exit as _exit
from os import environ, walk

class FontNotTTFError(Exception): pass

class CurriculumVitae(FPDF):

    def __init__(self, h_font: str, bg, calemoji: str='') -> None:
        super().__init__()
        self.bg=bg
        self.h_font: str = self._ttf(h_font)
        self.calemoji: str = chr(0x1F5D3) if not calemoji else calemoji
        self.date: str = datetime.today().strftime('%b %Y')
        self.header_text: str = f"{self.calemoji} {self.date}  "

        self.add_page()
        self.set_font(family='Courier', size=12)
        if self.bg:
            self.image(self.bg, 0, 8, w=210)
            self.set_text_color(255, 255, 255) 
        else:
            self.set_text_color(0)


    def _ttf(self, font) -> str:
    
        if not font.endswith('.ttf'):
            if '.' in font: raise FontNotTTFError
            else: font = font + '.ttf'
        return font

    def _font_path(self, paths: list[str]=[]) -> str:
    
        if not paths:
            HOME: str = environ['HOME']
            paths = [ 
                    HOME + '/.local/share/fonts/', 
                    HOME + '/.fonts',
                    '/usr/share/fonts/TTF/' 
                    ]
        
        for path in paths:
            for _, _, fonts in walk(path):
                if self.h_font in fonts:
                    return path + self.h_font
        raise LookupError('Font not found. Please specify an existing font')

    def header(self) -> None:
        '''
        Sets the header styling with a dark background that takes all the top
        of the page and has the current month and year at the right edge
        '''
        self.set_margin(0)
        self.add_font(self.h_font, fname=self._font_path())
        self.set_font(family=self.h_font, size=14)
        # The dark color for the header background
        self.set_fill_color(26, 28, 29) 
        # White color of the date on the header
        self.set_text_color(255, 255, 255) 
        self.cell(w=0, h=8, align='R',fill=True, txt=self.header_text)


    def text_column(self, file: str, l: int, y: int, w: int) -> None:
        '''
        Writes text to the cv by reading file content
        Args:
            file (str): the text file with the content of your CurriculumVitae
            l (int): how much space the text cell must be from the left margin
            y (int): the position of the text cell in the y coord on the page
            w (int): how wide the text cell must be
        '''
        with open(file) as fh:
            txt = fh.read()
        self.set_left_margin(l)
        self.set_y(y)
        self.multi_cell(w=w, align='L', txt=txt, markdown=True)
        self.ln(20)


def main(l_column_file: str, r_column_file: str, bg='',
        emoji_font: str ='Symbola', output_file='cv.pdf'):
    cv = CurriculumVitae(emoji_font, bg)
    cv.text_column(l_column_file, 20, 30, 100) # Big Column
    cv.text_column(r_column_file, 130, -180, 60) # Smaller right column

    try:
        cv.output(output_file)
        print('\nSaved', output_file)
    except:
        print('Something went wrong')
        _exit(1)

if __name__ == '__main__':

    main('curri-br', 'contact-skills', 'bg.jpg')
