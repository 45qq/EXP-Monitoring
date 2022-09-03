# -*- coding: UTF-8 -*-
import markdown
import os
from lib.config import root_dir
from bs4 import BeautifulSoup


exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
        'markdown.extensions.tables', 'markdown.extensions.toc']


def md_to_html(md_str):
    html_file = os.path.join(root_dir, 'lib', 'md.html')
    with open(html_file, 'r') as f:
        html = ''.join(f.readlines())
        ret = markdown.markdown(md_str, extensions=exts)
        return html % ret


def md_to_str(md_str):
    ret = markdown.markdown(md_str, extensions=exts)
    soup = BeautifulSoup(md_to_html(ret), 'html.parser')
    return ''.join(soup.body.findAll(text=True)).replace(' ∞', '').strip()


if __name__ == '__main__':
    print(md_to_html('# 123  \n---'))