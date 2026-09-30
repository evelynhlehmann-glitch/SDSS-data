from plotting import *
from classification import classify_star
from spectrum import *
from template_library import *
from coordsearch import *
from test import *

def run_demo():
    # cases = [
    #     (2934, 518),
    #     (2260, 143)
    # ]
    # for plate, fiberID in cases:
    #     # plotspectrum(plate, fiberID)
    #     plot_spectrum_and_template(plate, fiberID, template_info['A0'])

    # test_cases = [
    #     (3407, 367),
    #     (2260, 143),
    #     (3311, 27),
    #     (3311, 22),
    #     (1150, 221),
    #     (542, 514),
    #     (283, 120)
    # ]

    # for plate, fiberID in test_cases:
    #     classify_star(plate, fiberID, template_info)
    #     startype(plate, fiberID)
    #     print()

    # get_result(130, 40, 10, test = True)
    # startype(390, 115)
    test(50)

if __name__ == "__main__":
    run_demo()
    plt.show()