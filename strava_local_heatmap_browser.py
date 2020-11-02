# Copyright (c) 2019 Remi Salmon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# imports
import re
import glob
import argparse
import webbrowser

from folium import Map
from folium.plugins import HeatMap

# constants
HEATMAP_MAXZOOM = 16

HEATMAP_GRAD = {'dark':{0.0: '#000004',
                        0.1: '#160b39',
                        0.2: '#420a68',
                        0.3: '#6a176e',
                        0.4: '#932667',
                        0.5: '#bc3754',
                        0.6: '#dd513a',
                        0.7: '#f37819',
                        0.8: '#fca50a',
                        0.9: '#f6d746',
                        1.0: '#fcffa4'},
                 'light':{0.0: '#3b4cc0',
                          0.1: '#5977e3',
                          0.2: '#7b9ff9',
                          0.3: '#9ebeff',
                          0.4: '#c0d4f5',
                          0.5: '#dddcdc',
                          0.6: '#f2cbb7',
                          0.7: '#f7ac8e',
                          0.8: '#ee8468',
                          0.9: '#d65244',
                          1.0: '#b40426'}}

def get_gpx_files(args):
    gpx_filters = args.gpx_filters if args.gpx_filters else ['*.gpx']
    gpx_files = []
    for filter in gpx_filters:
        gpx_files += glob.glob('{}/{}'.format(args.gpx_dir, filter))
    
    if not gpx_files:
        exit('ERROR No GPX files in {}'.format(args.gpx_dir))

    return gpx_files

# functions
def main(args):
    if not args.output[-5:] == '.html':
        exit('ERROR Output file must be .html')

    heatmap_data = []

    for gpx_file in get_gpx_files(args):
        if not args.quiet:
            print('Reading {}'.format(gpx_file))

        with open(gpx_file, 'r') as file:
            for line in file:
                if '<trkpt' in line:
                    r = re.findall('[-]?[0-9]*[.]?[0-9]+', line)

                    heatmap_data.append([float(r[0]), float(r[1])])

    if not args.quiet:
        print('Loaded {} trackpoints'.format(len(heatmap_data)))

    if args.skip_ratio > 1:
        heatmap_data = heatmap_data[::args.skip_ratio]

        print('Reduced to {} trackpoints'.format(len(heatmap_data)))

    fmap = Map(tiles = 'CartoDB positron' if args.light_map else 'CartoDB dark_matter',
               prefer_canvas = True,
               max_zoom = HEATMAP_MAXZOOM)

    HeatMap(heatmap_data,
            radius = args.radius,
            blur = args.blur,
            gradient = HEATMAP_GRAD['light' if args.light_map else 'dark'],
            min_opacity = args.min_opacity,
            max_val = args.max_val).add_to(fmap)

    fmap.fit_bounds(fmap.get_bounds())

    fmap.save(args.output)

    if not args.quiet:
        print('Saved {}'.format(args.output))

    webbrowser.open(args.output, new = 2, autoraise = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate a local heatmap from Strava GPX files', epilog = 'Report issues to github.com/remisalmon/strava-local-heatmap-browser')

    parser.add_argument('--gpx-dir', metavar = 'DIR', default = 'gpx', help = 'directory containing the GPX files (default: gpx)')
    parser.add_argument('--gpx-filter', dest='gpx_filters', metavar = 'FILTER', action = 'append', help = 'glob filter for the GPX files (default: *.gpx)')
    parser.add_argument('--skip-ratio', metavar = 'N', type = int, default = 1, help = 'read every other N point of each GPX file (default: 1)')
    parser.add_argument('--light-map', action='store_true', help = 'use light map background')
    parser.add_argument('--output', metavar = 'FILE', default = 'strava_local_heatmap.html', help = 'output html file (default: strava_local_heatmap.html)')
    parser.add_argument('--radius', type = int, default = 2, help = 'radius of trackpoints in pixels (default: 2)')
    parser.add_argument('--blur', type = int, default = 2, help = 'amount of blur in pixels (default: 2)')
    parser.add_argument('--min-opacity', metavar = 'OPACITY', type = float, default = 0.3, help = 'minimum opacity value (default: 0.3)')
    parser.add_argument('--max-val', metavar = 'VAL', type = float, default = 1.0, help = 'maximum point intensity (default: 1.0)')
    parser.add_argument('--quiet', default = False, action = 'store_true', help = 'quiet output')

    args = parser.parse_args()

    main(args)
