from astropy.io import fits
from constants import template_files, template_names

def load_template(path):
    with fits.open(path) as hdul: 
        return hdul[0].data[0].copy(), hdul[0].header.copy()

templates = {name: load_template(f'spectemplatesDR2/{file}') 
             for name, file in zip(template_names, template_files)}