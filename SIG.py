import os
import bpy
renderscript = bpy.data.texts["renderscript.py"].as_module()

high_res = (1920, 1080)
medium_res = (1280, 720)
low_res = (720, 480)

# key: val list of tuple val[0]= rbeta range, val[1]= d range, val[2] = deform angle range ,val[3] = Displace strength range
bend_configuration = {"high": [(-35, 35), (0.45, 0.6), (30, 90), (0, 0)],
                      "medium": [(-40, 40), (0.47, 0.7), (-30, 30), (0, 0)],
                      "low": [(-20, 20), (0.5, 0.8), (-90, -30), (0, 0)],
                      "random": [(-40, 40), (0.45, 0.8), (-90, 90), (0, 0)]}

curve_configuration = {"high": [(-20, 20), (0.5, 0.7), (0, 0), (0.5, 0.8)],
                       "medium": [(-40, 40), (0.47, 0.7), (0, 0), (0.1, 0.5)],
                       "low": [(-30, 30), (0.5, 0.8), (0, 0), (-0.5, 0.1)],
                       "random": [(-40, 40), (0.47, 0.8), (0, 0), (-0.5, 0.5)]}

light_configuration = {"high": [20, 35], "medium": [10, 20], "low": [1, 10], "random": [1, 35]}


def bend(img, bbs_file, resolution=high_res, deform_axis="X", level="high", light_mod="random", quantity=20):
    """
    Generate bend images on the two side of image according to the given
    axi( X or Z). Z axi bend image across the length and X axi across the width.
    @param img: path to source image that we want to generate from
    @type img: all images types
    @param bbs_file: file containing the 4 coordinates of each word/letter bounding box in the img
    @type bbs_file: json
    @param resolution: resolution of the output images. built-in options high_res = 1920*1080,medium_res =1280x720,
    low_res = 720×480 accept also a custom resolution as int tuple of width*height. by default 1920*1080
    @type resolution: string or a int tuple
    @param deform_axis: the axi according to it we want to bend the image, X or Z by default X.
    @type deform_axis: string
    @param level: The bending angle range which will be uniformly distributed.There are 4 options high,medium,low,random
    @param light_mod: the power of the light in the scene.There are 4 options high,medium,low,random
    @type light_mod:string
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    """
    try:
        is_valid_path(img)
        is_valid_path(bbs_file)
    except:
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution)
    img_generator.set_scene(img)
    val = bend_configuration[level]
    mod = light_configuration[light_mod]
    img_generator.main_rendering_loop(bbs_file, val, mod, quantity, deform_axis)

def curve(img, bbs_file, resolution=high_res, level="medium", light_mod="random", quantity=20):
    """

    @param img:
    @type img:
    @param bbs_file:
    @type bbs_file:
    @param resolution:
    @type resolution:
    @param level:
    @type level:
    @param light_mod:
    @type light_mod:
    @param quantity:
    @type quantity:
    """
    try:
        is_valid_path(img)
        is_valid_path(bbs_file)
    except:
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution)
    img_generator.set_scene(img)
    val = curve_configuration[level]
    mod = light_configuration[light_mod]
    img_generator.main_rendering_loop(bbs_file, val, mod, quantity)


def fold(img, bbs_file, resolution=high_res, deform_axis="X", level="low", light_mod="random", quantity=20):
    try:
        is_valid_path(img)
        is_valid_path(bbs_file)
    except:
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution)
    img_generator.set_scene(img)
    img_generator.set_subdivision()
    val = bend_configuration[level]
    mod = light_configuration[light_mod]
    img_generator.main_rendering_loop(bbs_file, val, mod, quantity, deform_axis)


def bend_curve(img, bbs_file, resolution=high_res, deform_axis="X", bend_level="high", curve_level="low",
               light_mod="random", quantity=20):
    try:
        is_valid_path(img)
        is_valid_path(bbs_file)
    except:
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution)
    img_generator.set_scene(img)
    bend_val = bend_configuration[bend_level]
    curve_val = curve_configuration[curve_level]
    val = []
    val.append(intersection(list(bend_val[0]), list(curve_val[0])))
    val.append(intersection(list(bend_val[1]), list(curve_val[1])))
    val.append(bend_val[2])
    val.append(curve_val[3])
    mod = light_configuration[light_mod]
    img_generator.main_rendering_loop(bbs_file, val, mod, quantity, deform_axis)


def curve_fold(img, bbs_file, resolution=high_res, deform_axis="X", fold_level="high", curve_level="medium", light_mod="random",
               quantity=20):
    try:
        is_valid_path(img)
        is_valid_path(bbs_file)
    except:
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution)
    img_generator.set_scene(img)
    img_generator.set_subdivision()
    fold_val = bend_configuration[fold_level]
    curve_val = curve_configuration[curve_level]
    val = []
    val.append(intersection(list(fold_val[0]), list(curve_val[0])))
    val.append(intersection(list(fold_val[1]), list(curve_val[1])))
    val.append(fold_val[2])
    val.append(curve_val[3])
    mod = light_configuration[light_mod]
    img_generator.main_rendering_loop(bbs_file, val, mod, quantity, deform_axis)


def intersection(range1, range2):
    return (max(range1[0], range2[0]), min(range1[1], range2[1]))


def is_valid_path(path):
    if not os.path.exists(path):
        raise Exception(f"The file at {path} doesn't exist")


if __name__ == "__main__":
    bend_curve(r"C:\Users\safi_\Desktop\project\inputs\input_1.png", r"C:\Users\safi_\Desktop\project\inputs\input_1.json")
