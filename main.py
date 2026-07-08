from plotting import *
from classification import classify_star
from spectrum import startype
from templates import *

plotspectrum(2934, 518)
startype(2934, 518)

plot_spectrum_and_template(2934, 518, templates['B'])

plotspectrum(2260, 143)
startype(2260, 143)



classify_star(plate=3407, fiberID=367, templates_dict=templates)
startype(plate=3407, fiberID=367)

classify_star(plate=2260, fiberID=143, templates_dict=templates)
startype(plate=2260, fiberID=143)

classify_star(plate=2934, fiberID=518, templates_dict=templates)
startype(plate=2934, fiberID=518)

classify_star(plate=3856, fiberID=182, templates_dict=templates)
startype(3856, 182)

classify_star(plate=3311, fiberID=27, templates_dict=templates)
startype(3311, 27)

classify_star(plate=3311, fiberID=22, templates_dict=templates)
startype(3311, 22)

classify_star(plate=1150, fiberID=221, templates_dict=templates)
startype(1150, 221)

classify_star(plate=542, fiberID=514, templates_dict=templates)
startype(542, 514)

classify_star(plate=283, fiberID=120, templates_dict=templates)
startype(283, 120)

plt.show()
