from astroquery.sdss import SDSS
from plotting import *
from spectrum import *

startypes = ['O8%', 'O9%', 'B0%', 'B1%', 'B2%', 'B3%', 'B5%', 'B6%', 'B8%', 'B9%', 
    'A0%', 'A1%', 'A2%', 'A3%', 'A4%', 'A5%', 'A6%', 'A8%', 'A9%', 'F0%', 'F2%', 'F3%', 'F5%', 'F6%', 'F8%', 'F9%',
    'G0%', 'G1%', 'G2%', 'G3%', 'G4%', 'G5%', 'G8%', 'K0%', 'K1%', 'K2%', 'K3%', 'K4%', 'K5%', 'K7%',
    'M0%', 'M1%', 'M2%', 'M3%', 'M4%', 'M5%', 'M6%', 'M7%', 'M8%', 'M9%','L1%', 'Carbon%', 'wd%']

templates = ['O8', 'O9', 'B0', 'B1', 'B2', 'B3', 'B5', 'B6', 'B8', 'B9', 
    'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9', 'F0', 'F2', 'F3', 'F5', 'F6', 'F8', 'F9',
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
        AND snMedian >20
        AND zWarning = 0
        order by snMedian desc
        """
    res = query_sdss_sql(query, required_columns=["plate", "mjd", "fiberID", "subclass"])
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
    else:
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


# for subclass in startypes:
#     query = f"""
#         SELECT TOP 5
#         plate,
#         mjd,
#         fiberID,
#         subclass
#         FROM SpecObjAll
#         WHERE class = 'STAR'
#         AND subclass LIKE '{subclass}'
#         AND snMedian >20
#         AND zWarning = 0
#         order by snMedian desc
#         """
#     res = SDSS.query_sql(query)

#     if res is None or len(res) == 0:
#         del startemplate[f'{subclass}']
#         continue

#     spectra_list = []

#     for result in res:

#         plate = int(result["plate"])
#         fiber = int(result["fiberID"])

#         try:
#             spectra = SDSS.get_spectra(
#                 plate=plate,
#                 fiberID=fiber
#             )

#             sp = spectra[0]

#             wavelength, flux = get_spectrum_data(sp)

#             spectra_list.append((wavelength, flux))

#         except Exception as e:
#             print(f"Failed {subclass}: {e}")
#             continue


#     if len(spectra_list) == 0:
#         print(f"No usable spectra for {subclass}")
#         continue


#     # Normalize
#     normalized = []

#     for wavelength, flux in spectra_list:
#         normalized.append(normalize_flux(flux))


#     # Align wavelength grids
#     base_wave = spectra_list[0][0]

#     aligned = []

#     for (wavelength, flux) in zip(
#         [x[0] for x in spectra_list],
#         normalized
#     ):

#         interp = interp1d(
#             wavelength,
#             flux,
#             bounds_error=False,
#             fill_value=np.nan
#         )

#         aligned_flux = interp(base_wave)

#         aligned.append(aligned_flux)


#     # Median combine
#     template_flux = np.nanmedian(
#         aligned,
#         axis=0
#     )


#     template_info[startemplate[subclass]] = {
#         "wavelength": base_wave,
#         "flux": template_flux,
#         "count": len(aligned)
#     }
