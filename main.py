from plotting import *
from classification import classify_star
from spectrum import *
from template_library import *
from coordsearch import *

def run_demo():
    # cases = [
    #     (2934, 518),
    #     (2260, 143)
    # ]
    # for plate, fiberID in cases:
    #     # plotspectrum(plate, fiberID)
    #     plot_spectrum_and_template(plate, fiberID, template_info['F3'])

    test_cases = [
        (3407, 367),
        (2260, 143),
        (3311, 27),
        (3311, 22),
        (1150, 221),
        (542, 514),
        (283, 120)
    ]

    for plate, fiberID in test_cases:
        classify_star(plate, fiberID, template_info)
        startype(plate, fiberID)
        print()

    # get_result(175, 19, 5)
    # get_result(111, 40, 5)
    # startype(390, 115)

if __name__ == "__main__":
    run_demo()
    plt.show()