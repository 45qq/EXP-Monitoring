# -*- coding: UTF-8 -*-
import markdown
import os
from lib.config import root_dir


def md2html(mdstr):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']

    html_file = os.path.join(root_dir, 'lib', 'md.html')
    with open(html_file, 'r') as f:
        html = ''.join(f.readlines())
        ret = markdown.markdown(mdstr, extensions=exts)
        return html % ret


if __name__ == '__main__':
    print(md2html('# 123  \n---'))