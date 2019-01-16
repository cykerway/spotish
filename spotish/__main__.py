#!/usr/bin/env python3

'''
main module;
'''

from os.path import join
import argparse
import argparse_ext
import json
import logging
import logging_ext
import os
import requests
import spotipy
import spotipy.util
import sys

##  program name;
prog='spotish'

##  album cache;
album_cache = set()

##  track cache;
track_cache = set()

##  logger;
logger = logging_ext.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

def die(msg):

    '''
    die with a message;
    '''

    print('error: {}'.format(msg), file=sys.stderr)
    sys.exit(1)

def oplog(op_name, op_msg):

    '''
    log an operation;
    '''

    logger.v('[{:20s}]{}'.format(op_name, op_msg))

def parse_args():

    '''
    parse command line arguments;
    '''

    ##  init arg parser;
    parser = argparse.ArgumentParser(
        prog=prog,
        description='download tracks and playlists on spotify;',
        formatter_class=argparse_ext.HelpFormatter,
        add_help=False,
    )

    ##  add arg;
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='display help message;',
    )

    ##  add arg;
    parser.add_argument(
        '-u', '--user',
        type=str,
        metavar='user',
        help='spotify username;',
    )

    ##  add arg;
    parser.add_argument(
        '-i', '--client-id',
        type=str,
        metavar='id',
        help='client id;',
    )

    ##  add arg;
    parser.add_argument(
        '-s', '--client-secret',
        type=str,
        metavar='secret',
        help='client secret;',
    )

    ##  add arg;
    parser.add_argument(
        '-r', '--redirect-uri',
        type=str,
        metavar='uri',
        help='redirect uri;',
    )

    ##  add arg;
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='out',
        metavar='dir',
        help='output dir (default: out);',
    )

    ##  add arg;
    parser.add_argument(
        '--track-preview',
        action='store_true',
        help='download track preview;',
    )

    ##  add arg;
    parser.add_argument(
        '--album-image',
        action='store_true',
        help='download album image;',
    )

    ##  add arg;
    parser.add_argument(
        '--playlist-image',
        action='store_true',
        help='download playlist image;',
    )

    ##  add arg;
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='enable debug mode;',
    )

    ##  add arg;
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='enable verbose mode;',
    )

    ##  add arg;
    choices = ['tracks', 'playlists']
    parser.add_argument(
        'command',
        type=str,
        metavar='cmd',
        choices=choices,
        help='command ({});'.format(', '.join(choices)),
    )

    ##  parse args;
    args = parser.parse_args()

    return args

def save_playlist(args, playlist, playlist_uuid, playlist_dir):

    '''
    save playlist;
    '''

    ##  save playlist json;
    playlist_json = join(playlist_dir, playlist_uuid + '.json')
    oplog('save playlist', playlist_uuid)
    with open(playlist_json, 'wt') as fp:
        json.dump(playlist, fp, indent=4)

    ##  save playlist image;
    if args.playlist_image and playlist['images']:
        playlist_img = join(playlist_dir, playlist_uuid + '.jpg')
        oplog('save playlist image', playlist_uuid)
        resp_ = requests.get(playlist['images'][0]['url'])
        with open(playlist_img, 'wb') as fp:
            fp.write(resp_.content)

def save_album(args, album, album_uuid, album_dir):

    '''
    save album;
    '''

    ##  save album json;
    album_json = join(album_dir, album_uuid + '.json')
    oplog('save album', album_uuid)
    with open(album_json, 'wt') as fp:
        json.dump(album, fp, indent=4)

    ##  save album image;
    if args.album_image and album['images']:
        album_img = join(album_dir, album_uuid + '.jpg')
        oplog('save album image', album_uuid)
        resp_ = requests.get(album['images'][0]['url'])
        with open(album_img, 'wb') as fp:
            fp.write(resp_.content)

def save_track(args, track, track_uuid, track_dir):

    '''
    save track;
    '''

    ##  save track json;
    track_json = join(track_dir, track_uuid + '.json')
    oplog('save track', track_uuid)
    with open(track_json, 'wt') as fp:
        json.dump(track, fp, indent=4)

    ##  save track preview;
    if args.track_preview and track['preview_url']:
        track_preview = join(track_dir, track_uuid + '.mp3')
        oplog('save track preview', track_uuid)
        resp_ = requests.get(track['preview_url'])
        with open(track_preview, 'wb') as fp:
            fp.write(resp_.content)

def download_saved_tracks(sp, args):

    '''
    download saved tracks;
    '''

    ##  fetch saved tracks;
    limit = 50
    offset = 0
    while True:
        resp = sp.current_user_saved_tracks(limit=limit, offset=offset)

        ##  break when no more items;
        if len(resp['items']) == 0: break

        ##  config logger;
        if args.debug:
            logger.setLevel(logging_ext.DEBUG)
        elif args.verbose:
            logger.setLevel(logging_ext.VERBOSE)
        else:
            pass

        ##  dump raw json;
        logger.d(json.dumps(resp, indent=4))

        for item in resp['items']:
            ##  get track and album;
            track = item['track']
            album = track['album']

            ##  make track and album uuid;
            ##
            ##  `uri` guarantees uniqueness but isnt legible; `name` is legible
            ##  but doesnt guarantee uniqueness; uuid has both advantages;
            track_uuid = '{:02d}:{}:{}'.format(
                track['track_number'], track['uri'], track['name'])
            album_uuid = '{:02d}:{}:{}'.format(
                album['total_tracks'], album['uri'], album['name'])

            ##  make album dir;
            album_dir = join(args.output, album_uuid)
            os.makedirs(album_dir, exist_ok=True)

            ##  make track dir;
            track_dir = join(album_dir, track_uuid)
            os.makedirs(track_dir, exist_ok=True)

            ##  save album;
            if album['uri'] not in album_cache:
                album_cache.add(album['uri'])

                ##  save album;
                save_album(args, album, album_uuid, album_dir)

            ##  save track;
            if track['uri'] not in track_cache:
                track_cache.add(track['uri'])

                ##  save track;
                save_track(args, track, track_uuid, track_dir)

        ##  fetch next page;
        offset += limit

def download_playlist_tracks(sp, args, playlist_id, playlist_dir):

    '''
    download playlist tracks;
    '''

    limit = 50
    offset = 0
    while True:
        resp = sp.user_playlist_tracks(
            args.user, playlist_id, limit=limit, offset=offset)

        ##  break when no more items;
        if len(resp['items']) == 0: break

        logger.d(json.dumps(resp, indent=4))

        for i, item in enumerate(resp['items']):

            ##  get track;
            track = item['track']

            ##  make track uuid;
            track_uuid = '{:02d}:{}:{}'.format(
                i + 1, track['uri'], track['name'])

            ##  make track dir;
            track_dir = join(playlist_dir, track_uuid)
            os.makedirs(track_dir, exist_ok=True)

            ##  save track;
            save_track(args, track, track_uuid, track_dir)

        ##  fetch next page;
        offset += limit

def download_playlists(sp, args):

    '''
    download playlists;
    '''

    limit = 50
    offset = 0
    while True:
        resp = sp.current_user_playlists(limit=limit, offset=offset)

        ##  break when no more items;
        if len(resp['items']) == 0: break

        logger.d(json.dumps(resp, indent=4))

        for i, playlist in enumerate(resp['items']):
            ##  make playlist uuid;
            playlist_uuid = '{:02d}:{}:{}'.format(
                i + 1, playlist['uri'], playlist['name'])

            ##  make playlist dir;
            playlist_dir = join(args.output, playlist_uuid)
            os.makedirs(playlist_dir, exist_ok=True)

            ##  save playlist;
            save_playlist(args, playlist, playlist_uuid, playlist_dir)

            ##  download playlist tracks;
            download_playlist_tracks(sp, args, playlist['id'], playlist_dir)

        ##  fetch next page;
        offset += limit

def main():

    '''
    main function;
    '''

    ##  parse args;
    args = parse_args()

    if args.user is None:
        die('no user;')

    if args.client_id is None:
        die('no client id;')

    if args.client_secret is None:
        die('no client secret;')

    if args.redirect_uri is None:
        die('no redirect uri;')

    if args.output is None:
        die('no output dir;')

    ##  request access token;
    scope = ' '.join([
        'playlist-read-collaborative',
        'playlist-read-private',
        'user-library-read',
    ])

    token = spotipy.util.prompt_for_user_token(
        args.user,
        scope,
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=args.redirect_uri,
    )

    if token is None:
        die('cannot get token for {}'.format(args.user))

    ##  create spotipy client;
    sp = spotipy.Spotify(auth=token)

    ##  download;
    if args.command == 'tracks':
        download_saved_tracks(sp, args)
    elif args.command == 'playlists':
        download_playlists(sp, args)
    else:
        die('unknown command;')

if __name__ == '__main__':
    main()

