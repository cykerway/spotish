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

    1. Open Spotify and select the songs to export.
    2. Right click and choose 'Copy HTTP Link'.
    3. Paste into <listfile>.
    4. Run spotexp.py <listfile>.

----------------------------------------------------------------

Output format:

    [uri];[title];[time];[artist1,artist2...];[album]
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

        # url format: http://open.spotify.com/track/xxxxxxxxxxxxxxxxxxxxxx
        url = item.strip()

        # uri format: xxxxxxxxxxxxxxxxxxxxxx
        uri = url.split('/')[-1]

        # Download and parse HTML page.
        r, c = h.request(url, 'GET')
        root = etree.HTML(c)

        # Get album.
        album_node = root.xpath('//div[@class="h-data"]/h1[@class="h-title"]')[0]
        album = album_node.text

        song_node = root.xpath('//div/table/tbody/tr[@data-uri="spotify:track:{}"]'.format(uri))[0]

        # Get title.
        title_node = song_node.xpath('td/div/strong[@class="tl-name-name"]')[0]
        title = title_node.text

        # Get artists.
        artists_node = song_node.xpath('td/div/div[@class="tl-name-more text-muted"]')[0]
        artists = re.sub(r'\s*,\s*', ',', artists_node.text.strip())

        # Get time.
        time_node = song_node.xpath('td[@class="tl-cell tl-time"]/span')[0]
        time = time_node.text

        # Print result.
        result = ';'.join([uri, title, time, artists, album])
        print result.encode('UTF-8')

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

    download(sys.argv[1])
