from astroquery.sdss import SDSS
import numpy as np

def get_spectrum_data(spectrum):
    flux = spectrum[1].data['flux'].astype(np.float32)
    wavelength = 10 ** spectrum[1].data['loglam']
    return wavelength, flux

def startype(plate, fiberID):
    query = f"""
        select ra, dec, class, subclass            
        from specObjAll                      
        where plate = {plate}
        and fiberID = {fiberID}
    """
    res = SDSS.query_sql(query)
    # query = SDSS.query_specobj(plate=plate, fiberID=fiberID, fields=['ra', 'dec', 'class', 'subclass'])
    print(res)
    # This provides the SDSS recognized star type and is used only for testing purposes