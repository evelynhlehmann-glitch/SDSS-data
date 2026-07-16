from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from templates import *
from classification import classify_star
from plotting import *
from spectrum import startype


def get_result(value_ra, value_dec, max_results = 20, a = .1):
    query = f"""
        select top {max_results}                        
        ra, dec, plate, fiberID, class, subclass            
        from specObjAll                      
        where class = 'star'
        and ra > {value_ra - a}
        and ra < {value_ra + a}
        and dec > {value_dec - a}
        and dec < {value_dec + a}
    """
    res = SDSS.query_sql(query)
    if res is None:
        print("No spectra found")
    else:
        for star in res:
            plate = star['plate']
            fiber = star['fiberID']

            classify_star(plate, fiber, templates)
            startype(plate, fiber)