from pec_params import PecParams


def generate_in_file(pec_params, filename):
    s = str()
    s += "TITLE  " + pec_params.title + ".in\n"
    s += "       .\n"
    s += "GSTART >>>>>>>> Beginning of the geometry definition list.\n"
    for i in range(pec_params.layer_max_number):
        z = 0 if i == 0 else z + float(pec_params.layer_thickness[(i - 1)])/10000000
        s += "LAYER        %g\t\t+%g\t\t%d\n" % (
            z, (z + float(pec_params.layer_thickness[i])/10000000), (i + 1))
        for j in range(pec_params.body_max_number):
            s += "CENTRE\t\t0\t0\n"
            r = 0 if j == 0 else r + float(pec_params.ring_width[(j - 1)])/10000000
            s += "CYLIND\t%d\t%g\t%g\n" % (
                (i + 1), r, (r + float(pec_params.ring_width[j])/10000000))
    s += "GEND   <<<<<<<< End of the geometry definition list.\n"
    s += "       .\n"
    s += "       >>>>>>>> Source definition.\n"
    s += "SKPAR  1\n"
    s += "SENERG %d\n" % (pec_params.acceleration_voltage * 1000)
    s += "SPOSIT 0 0 0\n"
    s += "SCONE  0 0 0\n"
    s += "       .\n"
    s += "       >>>>>>>> Material data and simulation parameters.\n"
    for i in range(pec_params.layer_max_number):
        s += "MFNAME %s.mat\n" % pec_params.stack_material[i]
        s += "MSIMPA 50.0 50.0 50.0 0.0 0.0 0.0 -1.0\n"
    s += "       .\n"
    s += "       >>>>>>>> Dose and charge distributions.\n"
    for i in range(pec_params.layer_max_number):
        if pec_params.layer_dose[i] == 1:
            for j in range(pec_params.body_max_number):
                s += "DOSE2D %d %d %d %d\t[Tally 2D dose and charge dists. in body KL,KC]\n" % (
                    (i + 1), (j + 1), pec_params.slice_number[i], pec_params.bin_number[j])
            else:
                continue
    s += "       .\n"
    s += "       >>>>>>>> Job properties\n"
    s += "RESUME dump.dmp\n"
    s += "DUMPTO dump.dmp\n"
    s += "DUMPP  60\n"
    s += "       .\n"
    s += "NSIMSH %g\n" % pec_params.showers
    s += "TIME   %d\n" % pec_params.time
    s += "       .\n"
    s += "END"

    with open(filename, 'w+') as f:
        f.write(s)
    return s

def generate_stack_file(pec_params, filename):
    with open(filename, 'w+') as s:
        s.write("Material:\t%s\n" % str(pec_params.stack_material))
        s.write("Thickness [nm]:\t%s\n" % str(pec_params.layer_thickness))
        s.write("z resolution [nm]:\t%s\n" % str(pec_params.slice_thickness))
        s.write("\n")
        s.write("Calculation of dose distribution:\t%s\n" % str(pec_params.layer_dose))
        s.write("\n")
        s.write("Ring width [nm]:\t%s\n" % str(pec_params.ring_width))
        s.write("r resolution [nm]:\t%s\n" % str(pec_params.bin_width))
        s.write("\n")
        s.write("Number of simulated electrons:\t%d\n" % pec_params.showers)
        s.write("Electron injection energy [keV]:\t%d\n" % pec_params.acceleration_voltage)
        s.write("Allotted simulation time [s]:\t%d\n" % pec_params.time)

        
def generate_layer_file(pec_params, filename):
    with open(filename, 'w+') as l:
        l.write("Material:\t%s\n" % str(pec_params.stack_material).strip("[']").replace("', '", "\t"))
        l.write("Thickness [nm]:\t%s\n" % str(pec_params.layer_thickness).strip("[]").replace(", ", "\t"))

def generate_summary_file(pec_params, filename):
    with open(filename, 'w+') as u:
        for i in range(pec_params.layer_max_number):
            u.write("* Layer %d:\n\n" % (i + 1))
            u.write("\t%d nm %s (z resolution: %d nm)\n\n" % (
                pec_params.layer_thickness[i], pec_params.stack_material[i], pec_params.slice_thickness[i]))
            if pec_params.layer_dose[i] == 1:
                u.write("\tDose and charge distributions are calculated for this layer.\n\n")
        u.write("For all layers the same r resolution depending on r position is used:\n")
        for j in range(pec_params.body_max_number):
            r = 0 if j == 0 else r + pec_params.ring_width[(j - 1)]
            u.write("\t- %d nm for %d nm < r < %d nm\n" % (
                pec_params.bin_width[j], r, (r + pec_params.ring_width[j])))
        u.write("\n")
        u.write("Simulation of %d electrons with an injection energy of %d keV.\n" % (
            pec_params.showers, pec_params.acceleration_voltage))
        u.write("Allotted simulation time is %d s.\n\n" % pec_params.time)