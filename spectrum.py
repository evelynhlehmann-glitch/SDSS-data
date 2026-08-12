from astroquery.sdss import SDSS
import numpy as np
import shutil
import time
from pathlib import Path

def get_spectrum_data(spectrum):
    flux = spectrum[1].data['flux'].astype(np.float32)
    wavelength = 10 ** spectrum[1].data['loglam']
    return wavelength, flux


def _looks_like_skyserver_error(table):
    tokens = [str(name).lower() for name in table.colnames]
    for row in table:
        tokens.extend(str(value).lower() for value in row)
    blob = " ".join(tokens)
    return any(
        marker in blob
        for marker in (
            "<html",
            "<head",
            "<title",
            "skyserver error",
            "service unavailable",
            "bad gateway",
            "error occured",
            "error occurred",
        )
    )


def _clear_sdss_cache():
    cache_dir = Path(SDSS.cache_location)
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)


def query_sdss_sql(sql_query, *, retries=3, pause=2.0, required_columns=None):
    last_error = None
    for attempt in range(retries):
        try:
            result = SDSS.query_sql(sql_query, cache=(attempt == 0))
        except Exception as exc:
            last_error = exc
            time.sleep(pause * (attempt + 1))
            continue

        if result is None:
            return None

        missing = []
        if required_columns:
            missing = [col for col in required_columns if col not in result.colnames]

        if _looks_like_skyserver_error(result) or missing:
            _clear_sdss_cache()
            last_error = RuntimeError(
                "SDSS SkyServer returned an error page or incomplete table "
                f"(columns={result.colnames})"
            )
            print(f"SDSS query failed (attempt {attempt + 1}/{retries}), retrying...")
            time.sleep(pause * (attempt + 1))
            continue

        return result

    raise RuntimeError(f"SDSS SQL query failed after {retries} attempts") from last_error

def startype(plate, fiberID, return_value = False):
    query = f"""
        select ra, dec, class, subclass            
        from specObjAll                      
        where plate = {plate}
        and fiberID = {fiberID}
    """
    res = query_sdss_sql(query, required_columns=["subclass"])
    subclass = res['subclass']
    # query = SDSS.query_specobj(plate=plate, fiberID=fiberID, fields=['ra', 'dec', 'class', 'subclass'])
    if return_value == False:
        print(res)
    else:
        return subclass
    
    # This provides the SDSS recognized star type and is used only for testing purposes