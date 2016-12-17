#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2012 - 2015 Cyker Way
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

'''\
SpotExp - Spotify playlist exporter.

----------------------------------------------------------------

Usage:

1.  Open Spotify and select the songs to export.

2.  Right click the selected songs and choose *Copy Track Link*.

3.  Paste copied links into a text file named `listfile`.

4.  Run `spotexp.py listfile`.

----------------------------------------------------------------

Output format:

    <title>:<artist>:<album>:<duration>
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
        for line in f:

            # url format: http://open.spotify.com/track/xxxxxxxxxxxxxxxxxxxxxx
            url = line.strip()

            # uri format: xxxxxxxxxxxxxxxxxxxxxx
            uri = url.split('/')[-1]

            # Download and parse HTML page.
            r, c = h.request(url, 'GET')
            if (not r or r.get('status') != '200'):
                print('HTTP error.')
                exit(1)

            root = etree.HTML(c)

            # Get song metadata.
            title = root.xpath('//meta[@property="og:title"]')[0].attrib['content']
            artist = root.xpath('//a[@class="owner-name hdr-l"]')[0].text
            album = root.xpath('//a[@class="owner-name hdr-l"]')[1].text
            duration = root.xpath('//meta[@property="music:duration"]')[0].attrib['content']

            print(':'.join((title, artist, album, duration)), flush=True)

def usage(code):
    '''Echo usage and exit.'''

    usage_str = \
'''
Spotexp - Export playlists on Spotify.

Usage: spotexp.py <listfile>
'''
    print(usage_str)
    exit(code)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        usage(1)

    download(sys.argv[1])

