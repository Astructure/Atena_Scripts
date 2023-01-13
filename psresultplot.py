from matmodplot import savefig_nomargin
from simresultplot import *

# function which can return all folders name included in output directory
def subfolder_name_reader(output_dir):
    subfolders=[]
    for (root,dirs,files) in os.walk(output_dir): 
        subfolders.append(dirs)
    subfolders=subfolders[0]
    return subfolders



# psresultploter function extracting curves of Simresultploter_part2 function for all parametric studies 
# which are located in output_dir folder. this function plots the curve produced by simresultploter_part2 
# for all simulations inside each parametric study in just one fig.
# note that the output directory has several parameter study folders inside and each parameter study folder has several simulations inside
# note: Simresultploter_part2 function plots    1. Maxhoop stress, 
#                                               2. pullout curve, 
#                                               3. concrete reaction and 
#                                               4. yarn tensile stress un one fig for each simulation
def psresultploter(output_dir):
    paramstudies = subfolder_name_reader(output_dir)  
    for PS in paramstudies:
        ax1, ax1_1, ax1_2, axins, secax_x, secax_y= figspec_simresultploter_part2()
        ps_path = os.path.join(output_dir, PS)
        Simulations_name = subfolder_name_reader(ps_path)
        X_extraticks, Y_extraticks=[], []
        for sn in Simulations_name:
            path = os.path.join(ps_path, sn)
            xmax, ymax = simresultploter_part2(ax1, ax1_1, ax1_2, axins, path)
            X_extraticks.append(xmax)
            Y_extraticks.append(ymax)
        X_extraticks = list(set(X_extraticks)) # Repeated items should be deleted
        Y_extraticks = list(set(Y_extraticks)) 
        Y_extraticks = [max(Y_extraticks)]
        secax_x.set_xticks(X_extraticks)
        secax_y.set_yticks(Y_extraticks)
        savefig_nomargin(ps_path, 'results of {}'.format(PS))
        print('figs saved in {}'.format(ps_path))


# function runoverall_simresultploter_part1 runs the simresultploter_part1 function for all simulations inside 
# all parametric study folder inside output_dir folder folder.
# function simresultploter_part1 plots     1: plotting Tangential and Normal Stress profile along the interface
#                                          2: plotting Tangential and Normal Relative Displacements profile along the Interface     
#                                          3: plotting Relative Opening of Interface with respect to fixed end and with respect to loaded end'
#                                          4: plotting Normalized Opening of Interface with respect to fixed end and with respect to loaded end
#                                          5: plotting Normal Relative Displacements of Interface(opening) for all steps. focus is on profile
#                                             evolution and zoom in on the loaded end opening   
#                                          6: plotting Tangential and Normal Relative Displacements Evolution of Interface in selected nodes   
#                                          7: plotting Tangential and Normal stresses Evolution of Interface in selected nodes 
# 
def runoverall_simresultploter_part1(output_dir):
    paramstudies = subfolder_name_reader(output_dir)  
    for PS in paramstudies:
        ps_path = os.path.join(output_dir, PS)
        Simulations_name = subfolder_name_reader(ps_path)
        for name in Simulations_name:
                path = os.path.join(ps_path, name) 
                simresultploter_part1(path)


