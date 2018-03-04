import glob
import speakcommand
import random
import osc2

def read_files(is_train):
    fetch_type = "r"
    folder_names = [
        "AdditiveWave",
        "EmbeddedIteration",
        "IncrementDecrement",
        "Interpolate",
        "Perspective",
        "RadialGradient",
        "RandomGaussian",
        "Relativity",
        "Saturation"]
    if is_train == "t":
        all_origin_processing_file_pathes = glob.glob('data/origin/TOKKO/*.pde')
        #all_origin_processing_file_pathes = glob.glob('data/change/Blink/*.ino')
    else:
        all_origin_processing_file_pathes = glob.glob('data/change/Blink/*.ino')

    if fetch_type == "r":
        n_ran = random.randint(0,len(all_origin_processing_file_pathes))
        if n_ran == len(all_origin_processing_file_pathes):
            n_ran = 0
        origin_processing_file_pathes = [all_origin_processing_file_pathes[n_ran]]
    for p in origin_processing_file_pathes:
        f = open(p)
        lines = f.readlines()
        f.close()

    osc2.setup_osc(lines)
    return lines
