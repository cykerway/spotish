#!/usr/bin/python

'''
spotexp - A Spotify playlist exporter.
'''

import httplib2
import json
import os
import spotipy
import sys

from os.path import isdir
from os.path import join

USAGE_TEXT = '''
spotexp - A Spotify playlist exporter.

Usage: spotexp <list> <output>
'''

def download(infile, outdir):
    '''
    Download song metadata.

    Parameters
    ----------
    infile
        URL list file.

    outdir
        Output dir.
    '''
    sp = spotipy.Spotify()

    with open(infile, 'rt') as fin:
        for line in fin:
            # URI format: spotify:track:xxxxxxxxxxxxxxxxxxxxxx
            uri = line.strip()

            print(uri, flush=True)

            track = sp.track(uri)

            # Make output dir.
            uri_dir = join(outdir, uri)
            if not isdir(uri_dir):
                os.makedirs(uri_dir)

            # Dump song info.
            json_file = join(uri_dir, uri + '.json')
            with open(json_file, 'wt') as fout:
                json.dump(track, fout, indent=4)

def printerr(s=''):
    '''
    Print to stderr.
    '''
    print(s, file=sys.stderr, flush=True)

def usage():
    '''
    Display usage information.
    '''
    printerr(USAGE_TEXT)

def main():
    '''
    Main function.
    '''
    try:
        if len(sys.argv) != 3:
            raise Exception('invalid args')
        download(sys.argv[1], sys.argv[2])
    except Exception as e:
        printerr('Error: {}'.format(e))
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()

