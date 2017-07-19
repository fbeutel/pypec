class PecParams:
    def __init__(self):
        self.layer_max_number = 1 # number of layers in stack
        self.stack_material = [] # list of materials in stack (corresponding to layer sequence)
        self.layer_thickness = [] # list of layer thicknesses in [nm] (corresponding to layer sequence)
        self.slice_thickness = [] # list of slice thicknesses in [nm] per layer (corresponding to layer sequence)
        self.slice_number = [] # list of calculated number of slices per layer (corresponding to layer sequence), elements must be integers
        self.stack = [] # list containing entries alternating between material and thickness of layer, acceleration voltage is added as last element
        self.layer_dose = [] # list of layers for which dose and charge distributions are calculated or not
        self.title = ""
        
        ### bodies (sequence of list elements always starting in the shot centre)

        self.body_max_number = 3 # number of concentric bodies per layer
        self.body_radius = [100, 1000, 61000] # list of body radii in [nm] (corresponding to body sequence)
        self.ring_width = [100, 900, 60000] # list of ring widths in [nm] (corresponding to body sequence)
        self.bin_width = [1, 10, 300] # list of concentric bin widths in [nm] per body - r resolution (corresponding to body sequence)
        self.bin_number = [] # list of calculated number of bins per body (corresponding to body sequence), elements must be integers
        
        ### simulation parameters
        
        self.showers = 5e+06 # number of simulated showers (number of electrons)
        self.time = 100000 # "allotted simulation time" in [s]
        self.dump_file = "dump.dmp" # name of dump file (necessary for resuming simulation after break/abortion/shutdown)
        self.dump_period = 60 # period of time in [s] between each saving of simulation results to dump file

        
    def make_title(self):
        for i in range(len(self.stack_material)):
            self.title = str(self.stack_material[i]) + "_" + \
                         str(self.layer_thickness[i]) + "nm_" + self.title 

    def make_bodies(self):
        for j in range(self.body_max_number):
            r = 0 if j == 0 else r + self.ring_width[(j - 1)]
            print("\t%d nm for body %d (%d nm < r < %d nm)" % (
                    self.bin_width[j], (j + 1), r, (r + self.ring_width[j])))
            self.bin_number.append(self.ring_width[j] / self.bin_width[j])