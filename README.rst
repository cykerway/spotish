================================================
spotexp
================================================

.. default-role:: code

`spotext` is a Spotify metadata exporter.

Intro
================================================

`spotext` is a Spotify metadata exporter.

Usage
================================================

1.  Open Spotify and select tracks to export.

2.  Right click selected tracks and click *Copy Spotify URI*. This will copy
    Spotify URIs to clipboard.

3.  Paste copied links into a text file.

4.  Run spotexp as follows:

    ::

        spotexp <infile> <outdir>

    where:

    -   `infile` is the text file created in the previous step.

    -   `outdir` is the dir under which track metadata are written.

Output
================================================

`spotext` creates a subdir for each track and writes the following files in it:

-   `track.json`: Track metadata in JSON format.

-   `track.txt`: Simplified track metadata in TXT format.

-   `album.jpg`: Album cover.

Install
================================================

To install using `pip`, run:

::

    pip install spotexp

To install from source, run:

::

    python setup.py install --prefix=/usr

Dependency
================================================

`spotext` depends on `requests` and `spotipy`. Both can be installed using
`pip`.

License
================================================

The MIT License (MIT)

Copyright (c) 2012 Cyker Way

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

