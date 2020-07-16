# strava_local_heatmap_browser.py
Python script to reproduce the Strava Global Heatmap ([www.strava.com/heatmap](https://www.strava.com/heatmap)) with local GPX files

![screenshot.png](screenshot.png)

## Features

* Minimal Python dependencies ([folium](https://github.com/python-visualization/folium))
* Fast (3x faster than `gpxpy.parse()`)

## Usage

* Download your GPX files from Strava and add them to a `gpx` folder  
(see https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export)
* Run `python3 strava_local_heatmap_browser.py`

### Command-line options
```
usage: strava_local_heatmap_browser.py [-h] [--gpx-dir DIR]
                                       [--gpx-filter FILTER] [--output OUTPUT]
                                       [--radius RADIUS] [--blur BLUR]
                                       [--min-opacity MIN_OPACITY]
                                       [--max-val MAX_VAL] [--orange]
                                       [--blue-red] [--skip-ratio SKIP_RATIO]
                                       [--quiet]

optional arguments:
  -h, --help            show this help message and exit
  --gpx-dir DIR         directory containing the GPX files (default: gpx)
  --gpx-filter FILTER   glob filter for the GPX files (default: *.gpx)
  --output OUTPUT       output HTML file (default: strava_local_heatmap.html)
  --radius RADIUS       radius of trackpoints in pixels (default: 3)
  --blur BLUR           amount of blur in pixels (default: 3)
  --min-opacity MIN_OPACITY
                        minimum opacity value (default: 0.3)
  --max-val MAX_VAL     maximum point intensity (default: 1.0)
  --orange              use the orange gradient (this is the default)
  --blue-red            use the blue to green to red gradient
  --skip-ratio SKIP_RATIO
                        skip input points. ex. skip-ratio = 2 means use every-
                        other point. (default: 1)
  --quiet               quiet output

```

## Python dependencies
```
folium
```
