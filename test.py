from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from template_library import *
from classification import classify_star
from plotting import *
from spectrum import startype

def test(max_results = 50):
    query = f"""
        select top {max_results}                        
        ra, dec, plate, fiberID, class, subclass            
        from specObjAll                      
        where class = 'star'
        and (subclass like 'A%'
        or subclass like 'B%'
        or subclass like 'O%'
        or subclass like 'F%'
        or subclass like 'G%'
        or subclass like 'K%'
        or subclass like 'M%'
        or subclass like 'Carbon%'
        or subclass like 'wd%'
        or subclass like 'L1%')
        and snMedian > 25
        and zWarning = 0
    """
    res = SDSS.query_sql(query)

    exact_count = 0
    letter_count = 0
    total = 0

    for star in res:
        
        plate = star['plate']
        fiber = star['fiberID']
        subtype = star['subclass']
        result = classify_star(plate, fiber, template_info)

        if result is None:
            print()
            continue
        else:
            if result == subtype:
                exact_count += 1
            if result[0] == subtype[0]:
                letter_count += 1

            print(f"Actual: {subtype}")
            print()
            total += 1
    if total == 0:
        print("Why would total be 0")
    else:
        print(f"Exact result: {exact_count / total:.1%}")
        print(f"Letter result: {letter_count / total:.1%}")


if __name__ == "__main__":
    test(200)
