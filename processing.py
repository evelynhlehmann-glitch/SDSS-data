import numpy as np
from scipy.signal import medfilt, correlate, savgol_filter

from constants import SPECTRAL_LINES

def normalize(flux, wavelength, kernel_size=101):
    continuum = medfilt(flux.astype(np.float32), kernel_size=kernel_size)
    continuum[continuum == 0] = np.nan
    normalized_flux = flux / continuum
    return np.clip(normalized_flux, -3, 3)

def smooth_flux(flux, window_length=51, polyorder=2):
    return savgol_filter(flux, window_length=window_length, polyorder=polyorder)

def cross_correlation_score(a, b):
    a = (a - np.nanmean(a)) / np.nanstd(a)
    b = (b - np.nanmean(b)) / np.nanstd(b)
    corr = correlate(a, b, mode='valid')
    return -np.nanmax(corr)  # lower score is better

def get_feature_mask(wavelength, lines, window=20):
    mask = np.zeros_like(wavelength, dtype=bool)
    for line in lines.values():
        mask |= (wavelength >= line - window) & (wavelength <= line + window)
    return mask