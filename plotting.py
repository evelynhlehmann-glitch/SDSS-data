import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import interp1d
from astroquery.sdss import SDSS
import numpy as np

from constants import SPECTRAL_LINES
from spectrum import get_spectrum_data
from processing import normalize


def plot_spectral_lines(ax, lines_to_plot):
    colors = plt.cm.tab10.colors
    for i, (name, wavelength) in enumerate(lines_to_plot.items()):
        color = colors[i % len(colors)]
        ax.axvline(wavelength, color=color, linestyle=':', alpha=0.6, lw=1.2)
        trans = ax.get_xaxis_transform()
        ax.text(wavelength, 1.02, name, rotation =90, va= 'bottom', ha= 'center', fontsize = 6, color = color, alpha = 0.7, transform = trans)

    legend_lines = [Line2D([0], [0], color=colors[i % len(colors)], lw=1.5, linestyle=':') for i in range(len(lines_to_plot))]
    ax.legend(legend_lines, list(lines_to_plot.keys()), title="Spectral Lines", loc='upper right')

def plotspectrum(plate, fiberID):
    sp = SDSS.get_spectra(plate=plate, fiberID=fiberID)[0]
    wavelength, flux = get_spectrum_data(sp)

    plt.figure(figsize=(11,7))
    plt.plot(wavelength, flux, color='blue', lw=0.5)
    plot_spectral_lines(plt.gca(), {k: v for k, v in SPECTRAL_LINES.items() if wavelength.min() < v < wavelength.max()})
    
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux')
    plt.title(f'SDSS Spectrum - Plate {plate}, Fiber {fiberID}')
    plt.grid(alpha=0.3)

    plt.show()
    
    plt.figure(figsize=(11,7))
    plot_spectral_lines(plt.gca(), {k: v for k, v in SPECTRAL_LINES.items() if wavelength.min() < v < wavelength.max()})

    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux')
    plt.title(f'SDSS Normalized Spectrum - Plate {plate}, Fiber {fiberID}')
    plt.grid(alpha=0.3)
    norm_flux = normalize(flux, wavelength)
    plt.plot(wavelength, norm_flux, color='indigo', lw=0.5)
    plt.show()

def plot_spectrum_and_template(plate, fiberID, template):
    sp = SDSS.get_spectra(plate=plate, fiberID=fiberID)[0]
    obs_wavelength, obs_flux = get_spectrum_data(sp)
    obs_flux_norm = normalize(obs_flux, obs_wavelength)

    temp_flux = template[0].data[0]
    temp_header = template[0].header
    temp_loglam = temp_header['COEFF0'] + temp_header['COEFF1'] * np.arange(temp_flux.size)
    temp_wavelength = 10 ** temp_loglam

    interp_func = interp1d(temp_wavelength, temp_flux, bounds_error=False, fill_value=np.nan)
    temp_flux_interp = interp_func(obs_wavelength)
    temp_flux_norm = normalize(temp_flux_interp, obs_wavelength)

    plt.figure(figsize=(12, 7))
    plt.plot(obs_wavelength, obs_flux_norm, label='Observed Spectrum (Normalized)', color='blue', lw=0.5)
    plt.plot(obs_wavelength, temp_flux_norm, label='Template Spectrum (Normalized)', color='orange', lw=1)

    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Normalized Flux')
    plt.title(f'Continuum Normalized Comparison\nSDSS Plate {plate}, Fiber {fiberID}')
    plot_spectral_lines(plt.gca(), {k: v for k, v in SPECTRAL_LINES.items()
                                    if obs_wavelength.min() < v < obs_wavelength.max()})
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()