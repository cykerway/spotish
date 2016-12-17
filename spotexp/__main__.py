#!/usr/bin/python

'''
spotexp - A Spotify metadata exporter.
'''

import json
import os
import requests
import spotipy
import sys

from os.path import isdir
from os.path import join

USAGE_TEXT = '''
spotexp - A Spotify metadata exporter.

Usage: spotexp <infile> <outdir>
'''

def printout(s=''):
    '''
    Print to stdout with flush.
    '''
    print(s, file=sys.stdout, flush=True)

def printerr(s=''):
    '''
    Print to stderr with flush.
    '''
    print(s, file=sys.stderr, flush=True)

def dump(infile, outdir):
    '''
    Dump track metadata.

    Parameters
    ----------
    infile
        URL list file.

    outdir
        Output dir.

    Returns
    -------
    None
        None.
    '''
    sp = spotipy.Spotify()

    # Read input lines.
    with open(infile, 'rt') as fin:
        lines = fin.readlines()

    # Compute sequence number width.
    iwidth = len(str(len(lines)))

    for i, v in enumerate(lines):
        # URI format: spotify:track:xxxxxxxxxxxxxxxxxxxxxx
        uri = v.strip()

        # Print a notice.
        printout('({}/{}) {}'.format(
            str(i + 1).zfill(iwidth), str(len(lines)).zfill(iwidth), uri))

        # Get track info.
        track = sp.track(uri)

        # Make output dir for this track.
        uri_dir = join(outdir, uri)
        if not isdir(uri_dir):
            os.makedirs(uri_dir)

        # Dump track info in JSON format.
        json_file = join(uri_dir, 'track.json')
        with open(json_file, 'wt') as fout:
            json.dump(track, fout, indent=4)

        # Dump simplified track info in TXT format.
        txt_file = join(uri_dir, 'track.txt')
        with open(txt_file, 'wt') as fout:
            # Write track name.
            fout.write('name:{}\n'.format(track['name']))

            # Write track artists.
            for artist in track['artists']:
                fout.write('artist:{}\n'.format(artist['name']))

            # Write track album.
            fout.write('album:{}\n'.format(track['album']['name']))

            # Write track album artists.
            for artist in track['album']['artists']:
                fout.write('album-artist:{}\n'.format(artist['name']))

            # Write track duration.
            duration_ms = track['duration_ms']
            duration_hh = duration_ms // 3600000
            duration_ms -= duration_hh * 3600000
            duration_mm = duration_ms // 60000
            duration_ms -= duration_mm * 60000
            duration_ss = duration_ms // 1000
            duration_ms -= duration_ss * 1000
            fout.write('duration:{:02d}:{:02d}:{:02d}.{:03d}\n'.format(
                duration_hh, duration_mm, duration_ss, duration_ms
            ))

        # Download (the largest) album image.
        image_width = 0
        image_height = 0
        image_url = None
        for image in track['album']['images']:
            if image['width'] * image['height'] > \
               image_width * image_height:
                image_width = image['width']
                image_height = image['height']
                image_url = image['url']
        if image_url is not None:
            r = requests.get(image_url)
            if r.status_code != 200:
                raise Exception('HTTP error code {}'.format(r.status_code))
            image_file = join(uri_dir, 'album.jpg')
            with open(image_file, 'wb') as fout:
                fout.write(r.content)

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
        dump(sys.argv[1], sys.argv[2])
    except Exception as e:
        printerr('Error: {}'.format(e))
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()

