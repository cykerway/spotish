#!/usr/bin/python2
# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2012 Cyker Way
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''Spotexp - Export playlists on Spotify.

----------------------------------------------------------------

Usage:

    1. Open Spotify.
    2. Right click the playlist to export, choose 'Copy HTTP Link'.
    3. Paste into <listfile>.
    4. Run spotexp.py <listfile>.

----------------------------------------------------------------

Output format:

[title1]
[artist1]
[album1]
[title2]
[artist2]
[album2]
......
'''

import httplib2
import os
import re
import sys
import urllib
from lxml import etree

def download(listfile):
    '''Main download function.'''

    h = httplib2.Http()

    with open(listfile, 'rt') as f:
        items = f.readline().split()

    for item in items:
        url = item.strip()

        r, c = h.request(url, 'GET')

        root = etree.HTML(c)
        title_node = root.xpath('//div[@id="metadata"]/h1[@id="title"]/a[@id="title"]')[0]
        artist_node = root.xpath('//div[@id="metadata"]/div[@id="artist"]/p[@class="meta-info"]/a')[0]
        album_node = root.xpath('//div[@id="metadata"]/div[@id="album"]/p[@class="meta-info"]/a')[0]
        title, artist, album = title_node.text, artist_node.text, album_node.text

        print title
        print artist
        print album

def usage():
    '''Echo usage and exit.'''

    print '''\
Spotexp - Export playlists on Spotify.

Usage: spotexp.py <listfile>
'''
    exit(1)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()

    listfile = sys.argv[1]

    download(listfile)
