#!/usr/bin/env python
'''
File name: cv.py
Author: Diêgo Duarte
Date created: 2022/04/26
Python Version: 3.10.4
'''

from fpdf import FPDF
from datetime import datetime
from os import environ, walk

import sys


class FontNotTTFError(Exception): pass


class CurriculumVitae(FPDF):

    def __init__(self, 
            font: str='Courier', 
            bg: str='', 
            font_paths: list[str]=None) -> None: # type: ignore
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
        self.date: str = datetime.today().strftime('%b %Y')
        self.hdr_text: str = f"{self.date}  "

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
                if self.font in fonts:
                    return path + self.font
        raise LookupError('Font not found. Please specify an existing font')

    def header(self) -> None:
        '''
        Sets the header styling with a dark background that takes all the top
        of the page and has the current month and year at the right edge
        '''
        self.set_margin(0)
        self.set_font(family=self.font, size=14)
        # The dark color for the header background
        self.set_fill_color(26, 28, 29) 
        # White color of the date on the header
        self.set_text_color(255, 255, 255) 
        self.cell(w=0, h=8, align='R', 
                  fill=True, txt=self.hdr_text, 
                  markdown=True)

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
        self.multi_cell(w=w, align='J', txt=text, markdown=True)
        self.ln(20)


def main(*args, font: str='Courier', bg='', outfile='cv.pdf', footer=False):
    '''
    Args:
      *args (tuple(str, int, int, int)):
        args[0][0] must be the text to be written
        args[0][1:] are the position of the text cell on the page and its size
    '''

    cv = CurriculumVitae(font=font, bg=bg)
    for arg in args:
        cv.text_column(*arg)

    if footer:
        # Source Code link on the footer
        src_link = 'GPLv3 Source Code available at: ' +\
                'https://github.com/duartqx/cv-generator'
        cv.text_column(src_link, 36, 280, 160, size=9)

    try:
        cv.output(outfile)
        sys.stdout.write(f'\nSaved {outfile}\n\n')
        sys.stdout.flush()
    except:
        sys.stderr.write('\nSomething went wrong\n\n')
        sys.stderr.flush()
        sys.exit(1)


if __name__ == '__main__':

    from curri import curri_contabilizei as curri

    main((curri.body, 15, 25, 180), bg='bg.jpg', outfile='cv-diegoduarte.pdf')
