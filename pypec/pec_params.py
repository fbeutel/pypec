# pyPEC 0.x by Fabian Beutel (fabian.beutel@uni-muenster.de)
# Based on scripts by Silvia Diewald (silvia.diewald@kit.edu)

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

        self.relative_z = 0.5   # z in the center of the top layer
        self.target_z = None       # z value in nm

        self.acceleration_voltage = 100
        
    def make_title(self):
        for i in range(len(self.stack_material)):
            self.title = str(self.stack_material[i]) + "_" + \
                         str(self.layer_thickness[i]) + "nm_" + self.title
        self.title += str(self.acceleration_voltage) + "keV"

    def make_bodies(self):
        # Only select up to 9 bodies
        nlayers = int(9 / self.body_max_number)

        for i in range(len(self.stack_material)):
            if self.layer_thickness[i] <= 5:
                self.slice_thickness.append(1)
            elif 5 < self.layer_thickness[i] <= 50:
                self.slice_thickness.append(5)
            elif 50 < self.layer_thickness[i] <= 100:
                self.slice_thickness.append(10)
            elif 100 < self.layer_thickness[i] <= 1000:
                self.slice_thickness.append(25)
            else:
                self.slice_thickness.append(self.layer_thickness[i] / 10)
                
            self.layer_dose.append(1 if i < nlayers else 0)
            if self.layer_dose[i] == 1:
                print("For a %s layer thickness of %d nm, splitting into %d slices (each with a thickness of %d nm) is suggested." % (
                    self.stack_material[i], self.layer_thickness[i], (self.layer_thickness[i] / self.slice_thickness[i]), self.slice_thickness[i]))
                #input_var = raw_input("If you want to change the z resolution, please enter the desired slice thickness in nm.\n")
                #if input_var is not "" and int(input_var) > 0:
                #    slice_thickness[i] = int(input_var)
                #else:
                #    print("Default values are used.\n")
            self.slice_number.append(self.layer_thickness[i] / self.slice_thickness[i])
            print("Simulation parameters for layer %d: %d nm of %s, divided into %d slices of %d nm thickness.\n" % (
                (i + 1), self.layer_thickness[i], self.stack_material[i], self.slice_number[i],
                self.slice_thickness[i]))
            self.stack.extend([self.stack_material[i], self.layer_thickness[i]])
        
        for j in range(self.body_max_number):
            r = 0 if j == 0 else r + self.ring_width[(j - 1)]
            print("\t%d nm for body %d (%d nm < r < %d nm)" % (
                    self.bin_width[j], (j + 1), r, (r + self.ring_width[j])))
            self.bin_number.append(self.ring_width[j] / self.bin_width[j])
            
        if self.target_z is None:
            layer = int(self.relative_z)
            layer_z = self.relative_z - int(self.relative_z)
            self.target_z = 0
            for i in range(layer):
                self.target_z += self.layer_thickness[i]
                
            self.target_z += round(self.layer_thickness[layer] * layer_z)