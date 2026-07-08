from astropy.io import fits
from pathlib import Path
from constants import template_files, template_names

templates = {name: fits.open(f'/Users/evelyn/Downloads/spectemplatesDR2/{file}') for name, file in zip(template_names, template_files)}