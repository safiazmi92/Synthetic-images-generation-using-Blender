import os
from os.path import join, basename
import random
import yaml
import bpy
import sys

THIS_DIR = bpy.path.abspath("//")
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

renderscript = bpy.data.texts["renderscript.py"].as_module()


    
high_res = (1920, 1080)
medium_res = (1280, 720)
low_res = (720, 480)

# key: val list of tuple:
# val[0]= rbeta range, val[1]= d range, val[2] = deform angle range ,val[3] = Displace strength range

bend_up_configuration = {"high": [(-35, 35), (0.45, 0.6), (60, 90), (0, 0)],
                      "medium": [(-35, 35), (0.45, 0.6), (30, 60), (0, 0)],
                      "low": [(-40, 40), (0.47, 0.7), (0, 30), (0, 0)],
                      "random": [(-40, 40), (0.45, 0.7), (0, 90), (0, 0)],
                      "flat": [(-40, 40), (0.4, 0.8), (0, 0), (0, 0)]}


bend_down_configuration = {"high": [(-20, 20), (0.5, 0.8), (-90, -60), (0, 0)],
                      "medium": [(-20, 20), (0.5, 0.8), (-60, -30), (0, 0)],
                      "low": [(-40, 40), (0.47, 0.7), (-30, 0), (0, 0)],
                      "random": [(-40, 40), (0.47, 0.8), (-90, 0), (0, 0)],
                      "flat": [(-40, 40), (0.4, 0.8), (0, 0), (0, 0)]}

wrinkled_configuration = {"high": [(-20, 20), (0.5, 0.7), (0, 0), (0.5, 0.8)],
                          "medium": [(-40, 40), (0.47, 0.7), (0, 0), (0.1, 0.5)],
                          "low": [(-30, 30), (0.5, 0.8), (0, 0), (-0.5, 0.1)],
                          "random": [(-40, 40), (0.47, 0.8), (0, 0), (-0.5, 0.5)]}


def flat(generator, frames):
    generator.set_scene()
    val = bend_up_configuration["flat"]
    generator.main_rendering_loop(val, frames)


def bend(generator, level, deform_axis, quantity, bend_configuration):
    """
    Generate bend images on the two side of image according to the given
    axi( X or Z). Z axi bend image across the length and X axi across the width.
    @param deform_axis: the axi according to it we want to bend the image, X or Z by default X.
    @type deform_axis: char
    @param level: The bending angle range which will be uniformly distributed.There are 4 options high,medium,low,random
    The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength).
    @type level: list of 4- float tuples
    @param quantity: the quantity of image to generate.
    @type quantity: int
    """

    generator.set_scene()
    val = bend_configuration[level]
    img_generator.main_rendering_loop(val, quantity, deform_axis)


def wrinkled(img_generator, level, quantity):
    """
    Produce crumpled images with crease, shooting angle, lighting and background varying from image to image.
    @param level: The strength of the crease which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type level: list of 4- float tuples
    @param quantity: the quantity of image to generate.
    @type quantity: int
    """

    img_generator.set_scene()
    val = wrinkled_configuration[level]
    img_generator.main_rendering_loop(val, quantity)


def fold(img_generator, deform_axis, level, quantity):
    """
    Generate folded images which was folded in half as the shooting angle, lighting, folding angle and background varying
    from image to image.
    @param deform_axis: the axi according to it we want to fold the image, X or Z by default X.
    @type deform_axis: char
    @param level: The strength of the fold angle which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type level: list of 4- float tuples
    @param quantity: the quantity of image to generate. by default =/////
    @type quantity: int
    """

    img_generator.set_scene()
    img_generator.set_subdivision()
    val = bend_up_configuration[level]
    img_generator.main_rendering_loop(val, quantity, deform_axis)


def bend_wrinkled(img_generator, deform_axis, bend_level, wrinkle_level, quantity,bend_configuration):
    """
    Generate bend images with crease.The shooting angle, lighting, bend angele,crease strength and
    background varying from image to image.
    @param deform_axis: the axi according to it we want to bend the image, X or Z by default X.
    @type deform_axis: char
    @param bend_level: The bending angle range which will be uniformly distributed.There are 4 options
     high,medium,low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,
     bend_angle,wrinkled_strength)
    @type bend_level: list of 4- float tuples
    @param wrinkled_level: The strength of the crease which will be uniformly distributed.There are 4 options high,medium,
    low,random.The level is a list of 4-tuples ranges as (camera_angle_y_axi ,camera_height,bend_angle,wrinkled_strength)
    @type wrinkled_level:list of 4- float tuples
    @param quantity: the quantity of image to generate.
    @type quantity: int

    """

    img_generator.set_scene()
    bend_val = bend_configuration[bend_level]
    wrinkled_val = wrinkled_configuration[wrinkle_level]
    val = [intersection(list(bend_val[0]), list(wrinkled_val[0])), intersection(list(bend_val[1]), list(wrinkled_val[1])), bend_val[2],
           wrinkled_val[3]]
    img_generator.main_rendering_loop(val, quantity, deform_axis)


def intersection(range1, range2):
    return max(range1[0], range2[0]), min(range1[1], range2[1])


def is_valid_path(path):
    if not os.path.exists(path):
        raise Exception(f"The file at {path} doesn't exist")


def create_output_folder(image_path, out_put_path, fun_name):
    image_path = os.path.splitext(image_path)[0]
    img_name = basename(image_path)
    dir_name = fun_name + "_" + img_name
    dir_path = join(out_put_path, dir_name)
    try:
        os.mkdir(dir_path)
    except OSError as error:
        print(error)
    return dir_path

def create_arg_parser():
    # Creates and returns the ArgumentParser object

    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('inputYAMLfile',
                    help='Path to the input directory.')
    return parser

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    with open(argv[0]) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        input_files = data['input']
        images_folder = input_files['image_folder_path']
        json_folder = input_files['groundtruth_folder_path']
        output_file = data['output']['out_dir']
        if not os.path.exists(output_file):
            os.makedirs(output_file)
        samples = data['output']['num_samples_per_image']
        shape = data['shape']
        light_colors = data['light_colors']
        obj_shadow = data['object_shadow']
        res_1 = data['render_resolution_1']
        res_2 = data['render_resolution_2']
        res = (res_1,res_2)
        draw_mode = data['draw_labels']
        engine_name = data['render_engine']
        render_samples = data['render_samples']
        camera_rand = data['camera_random_mode']
        rotation_step = data['rotation_step']
        for image in os.listdir(images_folder):
            image_path = os.path.join(images_folder, image)
            json_path = os.path.join(json_folder,image)
            json_path = os.path.splitext(json_path)[0] + ".json"
            img_generator = renderscript.ImageGenerator(res, draw_mode, light_colors, obj_shadow,camera_rand,rotation_step)
            img_generator.load_document_image(image_path)
            img_generator.set_bbs(json_path)
            img_generator.set_render_engine(engine_name, render_samples)
            # flat shape
            flat_dict = shape['flat']
            quantity = int(flat_dict['probability'] * samples)
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "flat")
                img_generator.set_output_dir_path(output_dir)
                flat(img_generator, quantity)

            # bended_up shape
            bended_up = shape['bended_up']
            quantity = int(bended_up['probability'] * samples)
            level = bended_up['level']
            deform_axis = bended_up['side']
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "bended_up")
                img_generator.set_output_dir_path(output_dir)
                bend(img_generator, level, deform_axis, quantity,bend_up_configuration)

            # bended_down shape
            bended_down = shape['bended_down']
            quantity = int(bended_down['probability'] * samples)
            level = bended_down['level']
            deform_axis = bended_down['side']
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "bended_down")
                img_generator.set_output_dir_path(output_dir)
                bend(img_generator, level, deform_axis, quantity, bend_down_configuration)

            # wrinkled shape
            wrinkle = shape['wrinkled']
            quantity = int(wrinkle['probability'] * samples)
            level = wrinkle['level']
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "wrinkled")
                img_generator.set_output_dir_path(output_dir)
                wrinkled(img_generator, level, quantity)

            # folded shape
            folded_dict = shape['folded']
            quantity = int(folded_dict['probability'] * samples)
            level = folded_dict['level']
            deform_axis = folded_dict['side']
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "folded")
                img_generator.set_output_dir_path(output_dir)
                fold(img_generator, deform_axis, level, quantity)

            # mixed shape
            mixed = shape['mixed']
            bend_mode = mixed['bend_mode']
            if bend_mode == 'up':
                bend_config = bend_up_configuration
            else:
                bend_config= bend_down_configuration
            quantity = int(mixed['probability']*samples)
            bend_level = mixed['bend_level']
            wrinkle_level = mixed['wrinkle_level']
            deform_axis = mixed['bend_side']
            if quantity > 0:
                output_dir = create_output_folder(image_path, output_file, "mixed")
                img_generator.set_output_dir_path(output_dir)
                bend_wrinkled(img_generator, deform_axis, bend_level, wrinkle_level, quantity,bend_config)