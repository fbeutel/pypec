#!/usr/bin/env python

# v0.4 by SD (contact: silvia.diewald@kit.edu)

# compatibility

import sys

if sys.version_info[0] == 3: # looks for major python version
    raw_input = input # in python 3.x raw_input was renamed to input

# declaration of variables

## PENELOPE input file

def extract_xrz(target_z):
    
    ### title
    
    title = "" # name of the PENELOPE input and stack files without extension (.in/.stack)
    
    ### file names
    
    input_file = "" # name of the PENELOPE input file (.in)
    stack_material_file = [] # list of the PENELOPE .mat file names (corresponding to layer sequence)
    dose_distribution_file = "" # name of the dose distribution "dose-charge-xx.dat" files
    
    ### line parameter entries (read from .in file)
    
    acceleration_voltage = 50 # acceleration voltage in [kV]
    showers = 5e+06 # number of simulated showers (number of electrons)
    time = 100000 # "allotted simulation time" in [s]
    dump_file = "dump.dmp" # name of dump file (necessary for resuming simulation after break/abortion/shutdown)
    dump_period = 60 # period of time in [s] between each saving of simulation results to dump file
    
    ### line entry lists (read from .in file)
    
    layer_list = [] # list of LAYER entries (z_start, z_end, layer number)
    cylind_list = [] # list of CYLIND entries (layer number, r_start, r_end)
    dose2d_list = [] # list of DOSE2D entries (layer number, cylinder number, number of slices in layer, number of bins in body)
    
    ### line entry lists (read from dose-charge-xx.dat files)
    
    dose_charge_list = [] # list of entries (z [cm], r [cm], dose [eV/g], delta(dose) [eV/g], charge [e/cm^3], delta(charge) [e/cm^3])
    
    ### line parameter lists (read from PENELOPE .mat files)
    
    stack_material_density = [] # list of material densities in [g/cm^3] in stack (corresponding to layer sequence)
    
    ### stack (sequence of list elements always starting from top layer)
    
    layer_max_number = 1 # number of layers in stack
    stack_material = [] # list of materials in stack (corresponding to layer sequence
    layer_thickness = [] # list of layer thicknesses in [nm] (corresponding to layer sequence)
    slice_thickness = [] # list of calculated slice thicknesses in [nm] per layer (corresponding to layer sequence)
    slice_number = [] # list of number of slices per layer (corresponding to layer sequence), elements must be integers
    layer_dose = [] # list of layers for which dose and charge distributions are calculated or not
    
    ### bodies (sequence of list elements always starting in the shot centre)
    
    body_max_number = 1 # number of concentric bodies per layer
    stack_body_max_number = [] # list of number of concentric bodies per layer
    ring_width = [] # list of calculated ring widths in [nm] (corresponding to body sequence)
    stack_ring_width = [] # list of list of calculated ring widths in [nm] (corresponding to body sequence)
    body_radius = [] # list of body radii in [nm] (corresponding to body sequence)
    stack_body_radius = [] # list of list of body radii in [nm] (corresponding to body sequence)
    bin_width = [] # list of calculated concentric bin widths in [nm] per body - r resolution (corresponding to body sequence)
    stack_bin_width = [] # list of list of calculated concentric bin widths in [nm] per body - r resolution (corresponding to body sequence)
    bin_number = [] # list of number of bins per body (corresponding to body sequence), elements must be integers
    stack_bin_number = [] # list of list of number of bins per body (corresponding to body sequence), elements must be integers
    dose_distribution = [] # list of dose distribution number (corresponding to body sequence), elements must be integers
    stack_dose_distribution = [] # list of list of dose distribution number (corresponding to layer/body sequence), elements must be integers
    body_slice_number = [] # list of number of slices per body (corresponding to layer/body sequence), elements must be integers
    body_slice_thickness = [] # list of calculated slice thicknesses in [nm] per body (corresponding to layer/body sequence)
    body_layer_dose = [] # list of bodys for which dose and charge distributions are calculated or not
    body_bin_number = [] # list of number of bins per body (corresponding to layer/body sequence or not)
    body_bin_width = [] # list of calculated bin widths in [nm] per body (corresponding to layer/body sequence)
    
    ## GenISys extraction (.xrz) file
    
    ### file names
    
    extraction_file = "" # name of the GenISys extraction file (.xrz)
    
    ### directories
    
    dose_directory = "dose" # path to directory where all .xrz files are generated
    path_extraction_file = "" # path to .xrz files
    
    ### dose and charge distribution list
    
    material_dose_distribution = [] # list of relevant dose distribution entries (z in [nm], r in [um], "E" in [eV/um^3])
    material_charge_distribution = [] # list of relevant charge distribution entries (z in [nm], r in [um], "Q" in [e/cm^3])
    stack_charge_list = [] # list of integrated charges in [e/cm^2] (corresponding to layer sequence)
    stack_dose_list = [] # list of integrated doses in [eV/um^2] (corresponding to layer sequence)
    
    ## integrated charge (.charge) and (.dose) files
    
    ### file names
    
    layer_charge_file = "" # names of per slice integrated charge files (.charge)
    stack_charge_file = "" # name of per layer integrated charge file (.charge)
    layer_dose_file = "" # names of per slice integrated dose files (.dose)
    stack_dose_file = "" # name of per layer integrated dose file (.dose)
    
    ### directories
    
    path_layer_charge_file = "" # path to layer .charge files
    path_stack_charge_file = "" # path to stack .charge file
    path_layer_dose_file = "" # path to layer .dose files
    path_stack_dose_file = "" # path to stack .dose file
    
    ## indexes
    
    i = 0 # layer index (sequence starting from top layer), i < layer_max_number
    j = 0 # body index (sequence starting from centre body), j < body_max_number
    k = 0 # dose distribution index (sequence starting from top layer and center body)
    l = 0 # dose-charge distribution index
    
    line = 0 # line index in file
    
    z_vals = []
    
    ## read parameters from file
    
    import os
    
    for file in os.listdir(os.curdir):
        if file.endswith(".in"):
            input_file = file
    title = input_file.rstrip(".in")
    
    if os.path.isfile(input_file):
    
        print("... reading from %s ...\n" % input_file)
    
        r = open(input_file, 'r')
    
        for line in r:
            # generate raw parameter lists (containing strings)
            if line.startswith("LAYER"):
                layer_list.append(line.lstrip("LAYER").strip().split())
                # -> [layer start z value [cm], layer end z value [cm], layer number] (per layer)
            elif line.startswith("CYLIND"):
                cylind_list.append(line.lstrip("CYLIND").strip().split())
                # -> [layer number, start r value [cm], end r value [cm]] (per body)
            elif line.startswith("MFNAME"):
                stack_material_file.append(line.lstrip("MFNAME").strip())
                # -> [material file] (per layer)
            elif line.startswith("DOSE2D"):
                dose2d_list.append(line.lstrip("DOSE2D")
                            .rstrip("[Tally 2D dose and charge dists. in body KL,KC]\n")
                            .strip().split())
                # -> [layer number, cylinder number, number of slices, number of bins] (per body)
            # generate parameter values
            elif line.startswith("SENERG"):
                acceleration_voltage = (int(line.lstrip("SENERG").strip()) / 1000)
                # -> acceleration voltage [kV]
            elif line.startswith("DUMPTO"):
                dump_file = line.lstrip("DUMPTO").strip()
                # -> dump file
            elif line.startswith("DUMPP"):
                dump_period = int(line.lstrip("DUMPP").strip())
                # -> dump intervall
            elif line.startswith("NSIMSH"):
                showers = int(float(line.lstrip("NSIMSH").strip()))
                # -> number of simulated showers
            elif line.startswith("TIME"):
                time = int(line.lstrip("TIME").strip())
                # -> allotted simulation time [s]
    
        r.close()
    
        print("Simulation of %d electrons with an injection energy of %d keV.\n" % (
            showers, acceleration_voltage))
                
        layer_max_number = len(stack_material_file)
        print("Stack consists of %d layers:\n" % layer_max_number)
        for i in range(layer_max_number):
            # generate parameter lists (for layer i + 1)
            stack_material.append(stack_material_file[i].rstrip(".mat"))
            # -> [material name] (per layer)
            layer_thickness.append(int(1e7 * float(layer_list[i][1]))
                                   - int(1e7 * float(layer_list[i][0])))
            # -> [thickness [nm] of layer] (per layer)
            ring_width = [] # erase content -> entry for only one layer
            body_radius = [] # erase content -> entry for only one layer
            bin_number = [] # erase content -> entry for only one layer
            bin_width = [] # erase content -> entry for only one layer
            dose_distribution = [] # erase content -> entry for only one layer
            for j in range(len(cylind_list)):
                # generate parameter lists for all bodies in only one layer
                if int(cylind_list[j][0]) == (i + 1):
                    ring_width.append(int(1e7 * float(cylind_list[j][2]))
                                       - int(1e7 * float(cylind_list[j][1])))
                    # -> [ring width [nm] of cylinder] (per body within one layer)
                    body_radius.append(int(1e7 * float(cylind_list[j][2])))
                    # -> [outer radius [nm] of cylinder] (per body within one layer)
            body_max_number = len(body_radius) # entry for one layer
            stack_body_radius.append(body_radius[:]) # entries (lists) for all layers
            # -> [[outer radius [nm] of first cylinder, ..., outer radius [nm] of last cylinder]] (per layer) 
            stack_ring_width.append(ring_width[:]) # entries (lists) for all layers
            # -> [[ring width [nm] of first cylinder, ..., ring width [nm] of last cylinder]] (per layer)
            stack_body_max_number.append(body_max_number) # entries for all layers
            # -> [maximum number of bodies] (per layer)
            for j in range(len(dose2d_list)):
                # generate parameter lists for all bodies used for calculation
                # of charge distribution in all layers
                if int(dose2d_list[j][0]) == (i + 1):
                    body_slice_number.append(int(dose2d_list[j][2]))
                    # -> [number of slices] (per body with dose distribution calculated)
                    body_layer_dose.append(bool(1))
                    # -> [yes (dose distribution calculated)] (per body with dose distribution calculated)
                    body_bin_number.append(int(dose2d_list[j][3]))
                    # -> [number of bins] (per body with dose distribution calculated)
            # generate parameter lists with entries for all layers
            if any(dose_distribution_entry[0] == str(i + 1) for
                   dose_distribution_entry in dose2d_list):
                for dose_distribution_entry in dose2d_list:
                    # .index() raises a ValueError, using .find() instead
                    slice_number.append(int(body_slice_number
                                            [dose_distribution_entry[0]
                                             .find(str(i + 1))]))
                    # -> [number of slices] (per layer)
                    layer_dose.append(body_layer_dose[dose_distribution_entry[0]
                                                  .find(str(i + 1))])
                    # -> [yes (dose distribution calculated)] (per layer)
                    break # only one entry per layer needed
            else:
                slice_number.append(bool(0))
                # -> [no (no entry for number of slices necessary)] (per layer)
                layer_dose.append(bool(0))
                # -> [no (dose distribution not calculated)] (per layer)
            # generate parameter lists for all bodies in only one layer
            if any(dose_distribution_entry[0] == str(i + 1) for
                   dose_distribution_entry in dose2d_list):
                for k in range(len(dose2d_list)):
                    for j in range(body_max_number):
                        if (dose2d_list[k][0] == str(i + 1) and
                            dose2d_list[k][1] == str(j + 1)):
                            dose_distribution.append(k + 1)
                            # -> [number of dose-charge-xx.dat file] (per body within one layer)
                            bin_number.append(int(dose2d_list[k][3]))
                            # -> [number of bins] (per body within one layer)
                            bin_width.append(ring_width[j] / bin_number[j])
                            # -> [bin width [nm]] (per body within one layer)
            else:
                for j in range(body_max_number):
                    dose_distribution.append(bool(0))
                    # -> [no (no corresponding number of dose-charge-xx.dat file)] (per body within one layer)
                    bin_number.append(bool(0))
                    # -> [no (no entry for number of bins necessary)] (per body within one layer)
                    bin_width.append(bool(0))
                    # -> [no (no entry for width of bin necessary)] (per body within one layer)
            stack_dose_distribution.append(dose_distribution[:]) # entries (lists) for all layers
            # -> [[number of dose-charge-xx.dat file corresponding to first cylinder, ..., number of dose-charge-xx.dat file corresponding to last cylinder]] (per layer)
            stack_bin_number.append(bin_number[:]) # entries (lists) for all layers
            # -> [[number of bins in first cylinder, ..., number of bins in last cylinder]] (per layer)
            stack_bin_width.append(bin_width[:]) # entries (lists) for all layers
            # -> [[bin width [nm] in first cylinder, ..., bin width [nm] in last cylinder]] (per layer)
            # screen output
            print("* Layer %d:" % (i + 1))
            if layer_dose[i] == bool(1):
                slice_thickness.append(layer_thickness[i] / slice_number[i])
                # -> [slice thickness [nm]] (per layer)
                print("\t%d nm of %s with a z resolution of %d nm, " % (
                    layer_thickness[i], stack_material[i], slice_thickness[i]))
                print("\tdivided into %d concentric bodies with an r resolution of:" % (
                    stack_body_max_number[i]))
                for j in range(stack_body_max_number[i]):
                    print("\t- %d nm for %d nm < r < %d nm (-> dose-charge-0%d.dat)" % (
                        stack_bin_width[i][j],
                        0 if j == 0 else stack_body_radius[i][j - 1],
                        stack_body_radius[i][j],
                        stack_dose_distribution[i][j]))
            elif layer_dose[i] == bool(0):
                slice_thickness.append(bool(0))
                print("\t%d nm of %s" % (layer_thickness[i], stack_material[i]))
            print("")
    
    for i in range(layer_max_number):
    
        if os.path.isfile(stack_material_file[i]):
    
            print("... reading density from %s ...\n" % stack_material_file[i])
    
            mat = open(stack_material_file[i], 'r')
    
            for line in mat:
                # generate parameter values
                if line.startswith(" Mass density"):
                    stack_material_density.append(float(line
                                                        .lstrip(" Mass density =")
                                                        .rstrip("g/cm**3\n")
                                                        .strip()))
                    # -> [density [g/cm^3] of layer material] (per layer)
    
            mat.close()
    
        if layer_dose[i] == bool(1):
            dose_charge_list = [] # erase content -> entry for only one layer
            sort_material_dose_distribution = [] # erase content -> entry for only one layer
            material_dose_distribution = [] # erase content -> entry for only one layer
            sort_material_charge_distribution = [] # erase content -> entry for only one layer
            material_charge_distribution = [] # erase content -> entry for only one layer        
            
            for j in range(stack_body_max_number[i]):
                dose_distribution_file = ("dose-charge-0"
                                          + str(stack_dose_distribution[i][j])
                                          + ".dat")
    
                if os.path.isfile(dose_distribution_file):
    
                    print("... reading dose and charge distribution from %s ...\n" % (
                        dose_distribution_file))
    
                    dat = open(dose_distribution_file, 'r')
    
                    for line in dat:
                        if (line.startswith("   ") and not line.endswith("   \n")):
                            dose_charge_list.append(line.strip().split())
                            # -> [[z [cm], r [cm], dose [eV/g], uncertainty of dose [eV/g], charge [e/cm^3], uncertainty of charge [e/cm^3]]] (per line in all dose-charge-xx.dat files corresponding to the same layer)
    
                    dat.close()
    
            for l in range(len(dose_charge_list)):
                material_dose_distribution_entry = [] # erase content -> entry for only one "line"
                material_charge_distribution_entry = [] # erase content -> entry for only one "line"
                material_dose_distribution_entry.append(
                    round(1e7 * float(dose_charge_list[l][0]),4))
                material_dose_distribution_entry.append(
                    round(1e4 * float(dose_charge_list[l][1]),6))
                material_dose_distribution_entry.append(
                    1e-12 * stack_material_density[i]
                    * float(dose_charge_list[l][2]))
                material_dose_distribution.append(material_dose_distribution_entry)
                # -> [[z [nm], r [um], dose [eV/um^3]] (per line in all dose-charge-xx.dat files corresponding to the same layer)
                material_charge_distribution_entry.append(
                    round(1e7 * float(dose_charge_list[l][0]),4))
                material_charge_distribution_entry.append(
                    round(1e4 * float(dose_charge_list[l][1]),6))
                material_charge_distribution_entry.append(float(dose_charge_list[l][4]))          
                material_charge_distribution.append(material_charge_distribution_entry)
                # -> [[z [nm], r [um], charge [e/cm^3]] (per line in all dose-charge-xx.dat files corresponding to the same layer)
               
            sort_material_dose_distribution = sorted(material_dose_distribution)
            # -> [[*z [nm]*, r [um], dose [eV/um^3]] (per line in all dose-charge-xx.dat files corresponding to the same layer) 
            sort_material_charge_distribution = sorted(material_charge_distribution)
            # -> [[*z [nm]*, r [um], charge [e/cm^3]] (per line in all dose-charge-xx.dat files corresponding to the same layer) 
    
            if not os.path.isdir(dose_directory):
                os.makedirs(dose_directory)
    
            print("... extracting energy distribution for layer %d (%s) ...\n" % (
                i + 1, stack_material[i]))
    
    # output files
    
    ## generating .xrz files
    
            for l in range(len(sort_material_dose_distribution)):
                z_val = int(round(sort_material_dose_distribution[l][0], 0))
                if not z_val in z_vals:
                    z_vals.append(z_val)
                extraction_file = (title + "_" + str(z_val) + "nm.xrz")
                path_extraction_file = os.path.join(
                    dose_directory, extraction_file)
    
                if (sort_material_dose_distribution[l][0]
                    != sort_material_dose_distribution[(l - 1)][0]):
    
                    xrz = open(path_extraction_file, 'w+')
    
                xrz.write("%.4f\t%.5e\n" % (sort_material_dose_distribution[l][1],
                                            sort_material_dose_distribution[l][2]))
    
                if ((l + 1) == len(sort_material_dose_distribution)
                    or (sort_material_dose_distribution[l][0]
                        != sort_material_dose_distribution[(l + 1)][0])):
    
                    xrz.close()
    
                if (sort_material_dose_distribution[l][0] !=
                    sort_material_dose_distribution[(l - 1)][0]):
                    print("\t... z = %d nm ..." % (
                        round(sort_material_dose_distribution[l][0])))
    
            print("")
    
    ## generating .charge files
    
            sum_stack_charge = 0 # erase content -> entry for only one layer
            sum_stack_dose = 0 # erase content -> entry for only one layer        
            layer_charge_file = (title + "__" + str(i + 1) + "_"
                                 + stack_material[i] + ".charge")
            path_layer_charge_file = os.path.join(
                dose_directory, layer_charge_file)
    
            charge_layer = open(path_layer_charge_file, 'w+')
            
            for l in range(len(sort_material_charge_distribution)):
                if ((l == 0) or (sort_material_charge_distribution[l][0]
                                 != sort_material_charge_distribution[(l - 1)][0])):
                    sum_layer_charge = float(0) # erase content -> entry for only one z value
                    charge_layer.write("z = %d nm:\t" %
                                       round(sort_material_charge_distribution[l][0]))
                else:
                    sum_layer_charge = (sum_layer_charge
                                        + (1e-4 * (
                                            sort_material_charge_distribution[l][1] if
                                            l == 0 else
                                            (sort_material_charge_distribution[l][1]
                                             - sort_material_charge_distribution[l - 1][1]))
                                           * (sort_material_charge_distribution[l][2] if
                                              l == 0 else
                                              ((sort_material_charge_distribution[l][2] +
                                                sort_material_charge_distribution[l - 1][2])
                                               / 2))))
                    if ((l + 1) == len(sort_material_charge_distribution)
                        or (sort_material_charge_distribution[l][0]
                        != sort_material_dose_distribution[(l + 1)][0])):
                        charge_layer.write("%f e/cm^2\n" % sum_layer_charge)
                        sum_stack_charge = sum_stack_charge + sum_layer_charge
                          
            charge_layer.close()
    
            stack_charge_list.append(sum_stack_charge)
            # -> [sum of integrated charges [e/cm^2]] (per layer with charge distribution calculated)
               
            layer_dose_file = (title + "__" + str(i + 1) + "_"
                               + stack_material[i] + ".dose")
            path_layer_dose_file = os.path.join(
                dose_directory, layer_dose_file)
            
            dose_layer = open(path_layer_dose_file, 'w+')
    
            for l in range(len(sort_material_dose_distribution)):
                if ((l == 0) or (sort_material_dose_distribution[l][0]
                                 != sort_material_dose_distribution[(l - 1)][0])):
                    sum_layer_dose = float(0) # erase content -> entry for only one z value
                    dose_layer.write("z = %d nm:\t" %
                                       round(sort_material_dose_distribution[l][0]))
                else:
                    sum_layer_dose = (sum_layer_dose
                                       + (sort_material_dose_distribution[l][1] if
                                          l == 0 else
                                          (sort_material_dose_distribution[l][1]
                                           - sort_material_dose_distribution[l - 1][1])
                                          * (sort_material_dose_distribution[l][2] if
                                             l == 0 else 
                                             ((sort_material_dose_distribution[l][2] +
                                               sort_material_dose_distribution[l - 1][2])
                                              / 2))))
                    if ((l + 1) == len(sort_material_dose_distribution)
                        or (sort_material_dose_distribution[l][0]
                        != sort_material_dose_distribution[(l + 1)][0])):
                        dose_layer.write("%f eV/um^2\n" % sum_layer_dose)
                        sum_stack_dose = sum_stack_dose + sum_layer_dose
    
            dose_layer.close()
    
            stack_dose_list.append(sum_stack_dose)
            # -> [sum of integrated doses [eV/um^2]] (per layer with charge distribution calculated)
    
    
    stack_charge_file = (title + ".charge")
    path_stack_charge_file = os.path.join(
        dose_directory, stack_charge_file)
    
    charge_stack = open(path_stack_charge_file, 'w+')
        
    for i in range(layer_max_number):
        if layer_dose[i] == bool(1):
            charge_stack.write("Layer %d\t(%s):\t%d e/cm^2 (%f uC/cm^2)\n" % (
                i + 1, stack_material[i], stack_charge_list[i],
                (stack_charge_list[i] * 1.602176487e-13)))
            
    charge_stack.close()
    
    stack_dose_file = (title + ".dose")
    path_stack_dose_file = os.path.join(
        dose_directory, stack_dose_file)
    
    dose_stack = open(path_stack_dose_file, 'w+')
    
    for i in range(layer_max_number):
        if layer_dose[i] == bool(1):
            dose_stack.write("Layer %d\t(%s):\t%d eV/um^2\n" % (
                i + 1, stack_material[i], stack_dose_list[i]))
    
    dose_stack.close()
    
    
    
    # Extract distribution for z closest to the desired z value
    smallest_diff = -1
    selected_z = z_vals[0]
    for z in z_vals:
        diff = abs(z - target_z)
        if smallest_diff == -1 or diff < smallest_diff:
            smallest_diff = diff
            selected_z
            
    import shutil

    for file in os.listdir(dose_directory):
        if file.endswith("_" + str(selected_z) + "nm.xrz"):
            copy_file = file
            path_copy_file = os.path.join(dose_directory, copy_file)
            print("... copy %s ..." % copy_file)
            shutil.copy(path_copy_file, "../")
