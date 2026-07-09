from plotting import *
from classification import classify_star
from spectrum import startype
from templates import *

def run_demo():
    cases = [
        (2934, 518),
        (2260, 143)
    ]
    for plate, fiberID in cases:
        plotspectrum(plate, fiberID)
        plot_spectrum_and_template(plate, fiberID, templates['B'])

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
        classify_star(plate, fiberID, templates)
        startype(plate, fiberID)

if __name__ == "__main__":
    run_demo()
    plt.show()