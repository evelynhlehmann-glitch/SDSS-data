from astroquery.sdss import SDSS
from plotting import *
from spectrum import *

startypes = ['O8%', 'O9%', 'B0%', 'B1%', 'B2%', 'B3%', 'B5%', 'B6%', 'B8%', 'B9%', 
    'A0%', 'A1%', 'A2%', 'A4%', 'A5%', 'A6%', 'A8%', 'A9%', 'F0%', 'F2%', 'F3%', 'F5%', 'F6%', 'F8%', 'F9%',
    'G0%', 'G1%', 'G2%', 'G3%', 'G4%', 'G5%', 'G8%', 'K0%', 'K1%', 'K2%', 'K3%', 'K4%', 'K5%', 'K7%',
    'M0%', 'M1%', 'M2%', 'M3%', 'M4%', 'M5%', 'M6%', 'M7%', 'M8%', 'M9%','L1%', 'Carbon%', 'wd%']

templates = ['O8', 'O9', 'B0', 'B1', 'B2', 'B3', 'B5', 'B6', 'B8', 'B9', 
    'A0', 'A1', 'A2',  'A4', 'A5', 'A6', 'A8', 'A9', 'F0', 'F2', 'F3', 'F5', 'F6', 'F8', 'F9',
    'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G8', 'K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K7',
    'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9','L1', 'Carbon', 'wd']

startemplate = dict(zip(startypes, templates))


template_info = {}

for subclass in startypes:
    query = f"""
        SELECT TOP 1
        plate,
        mjd,
        fiberID,
        subclass
        FROM SpecObjAll
        WHERE class = 'STAR'
        AND subclass LIKE '{subclass}'
        """
    res = SDSS.query_sql(query)
    if res is None or len(res) == 0:
        del startemplate[f'{subclass}']
        continue

    result = res[0]

    plate = int(result["plate"])
    fiber = int(result["fiberID"])

    spectra = SDSS.get_spectra(plate=plate, fiberID=fiber)

    if spectra is None:
        print(f"No spectrum found for {subclass}: plate {plate}, fiber {fiber}")
        continue

    sp = spectra[0]

    wavelength, flux = get_spectrum_data(sp)
    template_info[startemplate[subclass]] = {
        "plate": plate,
        "fiber": fiber,
        "mjd": int(result["mjd"]),
        "subclass": str(result["subclass"]),
        "wavelength": wavelength,
        "flux": flux
    }