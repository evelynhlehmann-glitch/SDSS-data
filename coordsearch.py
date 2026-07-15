from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from templates import *
from classification import classify_star
from plotting import *
from spectrum import startype


def get_result(value_ra, value_dec, plot):
    coord = SkyCoord(ra=value_ra*u.degree, dec=value_dec*u.degree)
    result = SDSS.query_region(
        coord,
        radius=3*u.arcmin,
        spectro=True
    )
        
    if result is None:
        print("No spectra found.")
    else:
        result = result[:50]
        for star in result:
            plate = star['plate']
            fiber = star['fiberID']

            classify_star(plate, fiber, templates)
            startype(plate, fiber)
            if plot:
                plotspectrum(plate, fiber)