import os
import random
import bpy

renderscript = bpy.data.texts["renderscript.py"].as_module()

high_res = (1920, 1080)
medium_res = (1280, 720)
low_res = (720, 480)

# key: val list of tuple:
# val[0]= rbeta range, val[1]= d range, val[2] = deform angle range ,val[3] = Displace strength range
bend_configuration = {"high": [(-35, 35), (0.45, 0.6), (30, 90), (0, 0)],
                      "medium": [(-40, 40), (0.47, 0.7), (-30, 30), (0, 0)],
                      "low": [(-20, 20), (0.5, 0.8), (-90, -30), (0, 0)],
                      "random": [(-40, 40), (0.45, 0.8), (-90, 90), (0, 0)],
                      "flat": [(-40, 40), (0.4, 0.8), (0, 0), (0, 0)]}

wrinkled_configuration = {"high": [(-20, 20), (0.5, 0.7), (0, 0), (0.5, 0.8)],
                          "medium": [(-40, 40), (0.47, 0.7), (0, 0), (0.1, 0.5)],
                          "low": [(-30, 30), (0.5, 0.8), (0, 0), (-0.5, 0.1)],
                          "random": [(-40, 40), (0.47, 0.8), (0, 0), (-0.5, 0.5)]}


def flat(img, bbs_file, resolution=high_res, light_mod=True, quantity=50, draw=True):
    try:
        is_valid_path(img)
    except:
        print("Image Path doesn't exist")
        # return
    try:
        is_valid_path(bbs_file)
    except:
        print("Image Path doesn't exist")
        # return
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    val = bend_configuration["flat"]
    img_generator.main_rendering_loop(bbs_file, val, light_mod, quantity)


def bend(img, bbs_file, resolution=high_res, deform_axis="X", level="high", light_mod=True, quantity=50, draw=True):
    """
    Generate bend images on the two side of image according to the given
    axi( X or Z). Z axi bend image across the length and X axi across the width.
    @param img: path to source image that we want to generate from
    @type img: all images types
    @param bbs_file: file containing the 4 coordinates of each word/letter bounding box in the img
    @type bbs_file: json
    @param resolution: resolution of the output images. built-in options high_res = 1920*1080,medium_res =1280x720,
    low_res = 720×480 accept also a custom resolution as int tuple of width*height. by default 1920*1080
    @type resolution: int tuple
    @param deform_axis: the axi according to it we want to bend the image, X or Z by default X.
    @type deform_axis: char
    @param level: The bending angle range which will be uniformly distributed.There are 4 options high,medium,low,random
    The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength).
    @type level: list of 4- float tuples
    @param light_mod: the power of the light in the scene.There are 4 options high,medium,low,random
    @type light_mod:list of int with len = 2
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    @param draw: flag that if it equal True then draw the bbs on copy of the generated images and False do not. by default it equals False
    @type draw: bool
    """
    try:
        is_valid_path(img)
    except:
        print("Image Path doesn't exist")
        # return
    try:
        is_valid_path(bbs_file)
    except:
        print("Image Path doesn't exist")
        # return
        print("Path doesn't exist")
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    val = bend_configuration[level]
    img_generator.main_rendering_loop(bbs_file, val, light_mod, quantity, deform_axis)


def wrinkled(img, bbs_file, resolution=high_res, level="low", light_mod=True, quantity=50, draw=True):
    """
    Produce crumpled images with crease, shooting angle, lighting and background varying from image to image.
    @param img: path to source image that we want to generate from
    @type img: all images types
    @param bbs_file: file containing the 4 coordinates of each word/letter bounding box in the img
    @type bbs_file: json
    @param resolution: resolution of the output images. built-in options high_res = 1920*1080,medium_res =1280x720,
    low_res = 720×480 accept also a custom resolution as int tuple of width*height. by default 1920*1080
    @type resolution: int tuple
    @param level: The strength of the crease which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type level: list of 4- float tuples
    @param light_mod: the power of the light in the scene.There are 4 options high,medium,low,random
    @type light_mod: list of int with len = 2
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    @param draw: flag that if it equal True then draw the bbs on copy of the generated images and False do not. by default it equals False
    @type draw: bool
    """
    try:
        is_valid_path(img)
    except:
        print("Image Path doesn't exist")
        #return
    try:
        is_valid_path(bbs_file)
    except:
        print("Image Path doesn't exist")
        #return
        # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    val = wrinkled_configuration[level]
    img_generator.main_rendering_loop(bbs_file, val, light_mod, quantity)


def fold(img, bbs_file, resolution=high_res, deform_axis="X", level="high", light_mod=True, quantity=50, draw=True):
    """
    Generate folded images which was folded in half as the shooting angle, lighting, folding angle and background varying
    from image to image.
    @param img: path to source image that we want to generate from
    @type img: all images types
    @param bbs_file: file containing the 4 coordinates of each word/letter bounding box in the img
    @type bbs_file: json
    @param resolution: resolution of the output images. built-in options high_res = 1920*1080,medium_res =1280x720,
    low_res = 720×480 accept also a custom resolution as int tuple of width*height. by default 1920*1080
    @type resolution: int tuple
    @param deform_axis: the axi according to it we want to fold the image, X or Z by default X.
    @type deform_axis: char
    @param level: The strength of the fold angle which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type level: list of 4- float tuples
    @param light_mod: the power of the light in the scene.There are 4 options high,medium,low,random
    @type light_mod: list of int with len = 2
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    @param draw: flag that if it equal True then draw the bbs on copy of the generated images and False do not. by default it equals False
    @type draw: bool
    """
    try:
        is_valid_path(img)
    except:
        print("Image Path doesn't exist")
        # return
    try:
        is_valid_path(bbs_file)
    except:
        print("Image Path doesn't exist")
        # return
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    img_generator.set_subdivision()
    val = bend_configuration[level]
    img_generator.main_rendering_loop(bbs_file, val, light_mod, quantity, deform_axis)


def bend_wrinkled(img, bbs_file, resolution=high_res, deform_axis="X", bend_level="high", wrinkled_level="low",
                  light_mod=True, quantity=50, draw=True):
    """
    Generate bend images with crease.The shooting angle, lighting, bend angele,crease strength and
    background varying from image to image.
     @param img: path to source image that we want to generate from
    @type img: all images types
    @param bbs_file: file containing the 4 coordinates of each word/letter bounding box in the img
    @type bbs_file: json
    @param resolution: resolution of the output images. built-in options high_res = 1920*1080,medium_res =1280x720,
    low_res = 720×480 accept also a custom resolution as int tuple of width*height. by default 1920*1080
    @type resolution: int tuple
    @param deform_axis: the axi according to it we want to bend the image, X or Z by default X.
    @type deform_axis: char
    @param bend_level: The bending angle range which will be uniformly distributed.There are 4 options
     high,medium,low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,
     bend_angle,wrinkled_strength)
    @type bend_level: list of 4- float tuples
    @param wrinkled_level: The strength of the crease which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type wrinkled_level:list of 4- float tuples
    @param light_mod: the power of the light in the scene.There are 4 options high,medium,low,random
    @type light_mod: list of int with len = 2
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    @param draw: flag that if it equal True then draw the bbs on copy of the generated images and False do not. by default it equals False
    @type draw: bool

    """
    try:
        is_valid_path(img)
    except:
        print("Image Path doesn't exist")
        # return
    try:
        is_valid_path(bbs_file)
    except:
        print("Image Path doesn't exist")
        # return
    # TODO check if parameter are valid res & axi & light & quantity
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    bend_val = bend_configuration[bend_level]
    wrinkled_val = wrinkled_configuration[wrinkled_level]
    val = []
    val.append(intersection(list(bend_val[0]), list(wrinkled_val[0])))
    val.append(intersection(list(bend_val[1]), list(wrinkled_val[1])))
    val.append(bend_val[2])
    val.append(wrinkled_val[3])
    img_generator.main_rendering_loop(bbs_file, val, light_mod, quantity, deform_axis)

def gen_with_obj(img, bbs_file, resolution=high_res, draw=False, obj = 'plant'):
    img_generator = renderscript.ImageGenerator(resolution, draw)
    img_generator.set_scene(img)
    img_generator.unable_object_render(obj)
    img_generator.set_object_in_scene(obj)
    #img_generator.main_rendering_loop(bbs_file, bend_configuration["flat"])
    level = random.choice(list(bend_configuration.values()))
    img_generator.main_rendering_loop(bbs_file, level, True, obj_mod=obj)
    level = random.choice(list(wrinkled_configuration.values()))
    img_generator.main_rendering_loop(bbs_file, level, False, obj_mod=True)

def intersection(range1, range2):
    return (max(range1[0], range2[0]), min(range1[1], range2[1]))


def is_valid_path(path):
    if not os.path.exists(path):
        raise Exception(f"The file at {path} doesn't exist")


if __name__ == "__main__":
    arr = ['3.jpg', '4.jpeg', '5.png','11.jpg']
    arr1 = ['3', '4', '5','11']
    for i in range(6):
        path = "C:\\Users\\safi_\\Desktop\\project\\inputs\\" + arr[i]
        jpath = "C:\\Users\\safi_\\Desktop\\project\\inputs\\" + arr1[i] + ".json"
        gen_with_obj(path,jpath)
        #fold(path,jpath)
        #bend(path, jpath)
        #bend_wrinkled(path, jpath, light_mod=False, quantity=20, draw=False)
        #bend_wrinkled(path, jpath)Y