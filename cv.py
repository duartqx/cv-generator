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

    def __init__(self, font: str='Courier', h_font: str='', 
            calemoji: str='', bg: str='', font_paths: list[str]=None) -> None:
        '''
        Instantiates the CurriculumVitae class
        Args
            font (str): the font family you want to use for the body text
            bg (str): the background image name, defaults to an empty string,
            leave it at that if you want a normal white background
            h_font (str): the name of the font you want to use on the header,
            needs to be an emoji font if you want the calendar emoji on the
            header. defaults to an empty string
            calemoji (str): the calendar emoji to be shown before the date on
            the header bar, defaults to 1F5D3 emoji
        '''
        super().__init__()
        self.bg: str = bg
        self.font: str = font
        self.font_paths = font_paths
        self.h_font: str = self._ttf(h_font)
        self.calemoji: str = chr(0x1F5D3) if not calemoji else calemoji
        self.date: str = datetime.today().strftime('%b %Y')
        self.header_text: str = f"{self.calemoji} {self.date}  "

        self.add_page()

        if self.bg:
            self.image(self.bg, 0, 8, w=210)
            self.set_text_color(255, 255, 255) 
        else:
            self.set_text_color(0)

    def _ttf(self, font: str) -> str:
    
        if not font.endswith('.ttf'):
            if '.' in font: raise FontNotTTFError
            else: font = font + '.ttf'
        return font

    def _font_path(self) -> str:
    
        if self.font_paths is None:
            HOME: str = environ['HOME']
            self.font_paths = [ 
                    HOME + '/.local/share/fonts/', 
                    HOME + '/.fonts',
                    '/usr/share/fonts/TTF/' 
                    ]
        
        for path in self.font_paths:
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

    def text_column(self, text: str, 
                    l: int, y: int, w: int, 
                    size: int=12) -> None:
        '''
        Writes text to the cv
        Args:
            file (str): the text file with the content of your CurriculumVitae
            l (int): how much space the text cell must be from the left margin
            y (int): the position of the text cell in the y coord on the page
            w (int): how wide the text cell must be
        '''
        self.set_font(family=self.font, size=size)
        self.set_left_margin(l)
        self.set_y(y)
        self.multi_cell(w=w, align='L', txt=text, markdown=True)
        self.ln(20)


def main(l_column_text: str, r_column_text: str, 
        font: str='Courier', emoji_font: str ='Symbola',
        bg='',  output_file='cv.pdf', footer=False):

    cv = CurriculumVitae(font=font, h_font=emoji_font, bg=bg)
    cv.text_column(l_column_text, 20, 30, 100) # Big Column
    cv.text_column(r_column_text, 130, 110, 60) # Smaller right column

    if footer:
        # Source Code link on the footer
        src_link = 'GPLv3 Source Code available at: ' +\
                'https://github.com/duartqx/cv-generator'
        cv.text_column(src_link, 36, 280, 160, size=9)

    try:
        cv.output(output_file)
        print('\nSaved', output_file, '\n')
    except:
        print('Something went wrong')
        _exit(1)

if __name__ == '__main__':

    import curri_br
    #import curri_en

    main(curri_br.body_x, curri_br.side_info, bg='bg.jpg')
