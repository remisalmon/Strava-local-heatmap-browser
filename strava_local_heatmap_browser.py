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
import argparse
import glob
import re
import webbrowser

from folium import Map
from folium.plugins import HeatMap

# functions
def main(args):
    # arguments
    gpx_dir = args.dir
    gpx_filter = args.filter
    html_file = args.output
    heatmap_radius = args.radius
    heatmap_blur = args.blur

    if not html_file[-5:] == '.html':
        print('ERROR: output file must be .html')
        quit()

    # parse GPX files
    gpx_files = glob.glob(gpx_dir+'/'+gpx_filter)

    if not gpx_files:
        print('ERROR: no GPX files in '+gpx_dir)
        quit()

    heatmap_data = []

    for gpx_file in gpx_files:
        print('reading '+gpx_file+'...')

        with open(gpx_file, 'r') as file:
            for line in file:
                if '<trkpt' in line:
                    tmp = re.findall('-?\d*\.?\d+', line)

                    heatmap_data.append([float(tmp[0]), float(tmp[1])])

    print('read '+str(len(heatmap_data))+' trackpoints')

    # color map
    heatmap_grad = \
    {0.0: '#000003',
     0.1: '#160b39',
     0.2: '#410967',
     0.3: '#6a176e',
     0.4: '#932567',
     0.5: '#bb3754',
     0.6: '#dc5039',
     0.7: '#f37719',
     0.8: '#fba40a',
     0.9: '#f5d745',
     1.0: '#fcfea4'}

    # create Folium map
    fmap = Map(tiles = 'CartoDB dark_matter')

    HeatMap(heatmap_data, radius = heatmap_radius, blur = heatmap_blur, gradient = heatmap_grad).add_to(fmap)

    fmap.fit_bounds(fmap.get_bounds())

    # save map to HTML file and open with browser
    print('writing '+html_file+'...')

    fmap.save(html_file)

    webbrowser.open(html_file, new = 2, autoraise = True)

    print('done')

if __name__ == '__main__':
    # command line parameters
    parser = argparse.ArgumentParser(description = 'Generate a local heatmap from Strava GPX files', epilog = 'Report issues to https://github.com/remisalmon/strava-local-heatmap-browser')
    parser.add_argument('--gpx-dir', dest = 'dir', default = 'gpx', help = 'directory containing the GPX files (default: gpx)')
    parser.add_argument('--gpx-filter', dest = 'filter', default = '*.gpx', help = 'regex filter for the GPX files (default: *.gpx)')
    parser.add_argument('--output', dest = 'output', default = 'strava_local_heatmap.html', help = 'output HTML file (default: strava_local_heatmap.html)')
    parser.add_argument('--radius', dest = 'radius', type = int, default = 3, help = 'radius of trackpoints in pixels (default: 3)')
    parser.add_argument('--blur', dest = 'blur', type = int, default = 3, help = 'amount of blur in pixels (default: 3)')

    args = parser.parse_args()

    main(args)
