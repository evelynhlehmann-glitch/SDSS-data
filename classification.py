import numpy as np
from scipy.interpolate import interp1d
from astroquery.sdss import SDSS
from constants import *
from spectrum import *
from processing import *

def classify_star(plate, fiberID, templates_dict, min_overlap_frac=0.75):
    sp = SDSS.get_spectra(plate=plate, fiberID=fiberID)[0]
    obs_wavelength, obs_flux = get_spectrum_data(sp)


    obs_flux_norm = normalize(obs_flux, obs_wavelength)

    best_match = None
    best_score = np.inf

    for star_type, template in templates_dict.items():
        temp_flux = template[0].data[0]
        temp_flux = smooth_flux(temp_flux, window_length=51)
        temp_header = template[0].header
        temp_loglam = temp_header['COEFF0'] + temp_header['COEFF1'] * np.arange(temp_flux.size)
        temp_wavelength = 10 ** temp_loglam

        common_min = max(obs_wavelength.min(), temp_wavelength.min())
        common_max = min(obs_wavelength.max(), temp_wavelength.max())
        in_common = (obs_wavelength >= common_min) & (obs_wavelength <= common_max)

        if in_common.sum() < min_overlap_frac * len(obs_wavelength):
            continue

        obs_wl_common = obs_wavelength[in_common]
        obs_flux_common = obs_flux_norm[in_common]

        interp = interp1d(temp_wavelength, temp_flux, bounds_error=False, fill_value=np.nan)
        temp_flux_norm = normalize(interp(obs_wl_common), obs_wl_common)

        feature_mask = get_feature_mask(obs_wl_common, SPECTRAL_LINES, window=20)

        obs_feat_flux = obs_flux_common[feature_mask]
        temp_feat_flux = temp_flux_norm[feature_mask]

        valid_mask = ~np.isnan(obs_feat_flux) & ~np.isnan(temp_feat_flux)

        if valid_mask.sum() == 0:
            continue

        score = cross_correlation_score(obs_feat_flux[valid_mask], temp_feat_flux[valid_mask])

        if score < best_score:
            best_score = score
            best_match = star_type

    if best_match is not None:
        print(f"Best Match: {best_match} (Score={best_score:.5f})")
        print(' ')
        return best_match
    else:
        print("No close match.")
        return None