# unheatmap
Unheatmap - get data from heatmaps

Supports log scale

# Usage
call
```
./unheatmap.py heatmap.png
```
* first two clicks set the position of the color-scale
* further clicks let you pick a point and get the value from the map.
* Keys can be used to adjust the position after a click

# Requirements
* Pillow for python 3 including tk buildings
Install e.g. with
```
dnf install python3-pillow-tk
```