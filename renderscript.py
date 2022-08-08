
import bpy
import os
import sys
from os.path import join
import numpy as np
import math as m
import random
import json
from pathlib import Path
from math import radians
from mathutils import Vector
from random import uniform, triangular
from PIL import Image, ImageDraw

gen_bbs = bpy.data.texts["gen_bbs.py"].as_module()
light_types = ["POINT", "SUN", "SPOT"]
sun_colors = {"white": (1.0, 1.0, 1.0), "yellow_red": (1.0, 0.571187, 0.140428), "yellow_white": (1.0, 0.943264, 0.373584),
              "violet": (1.0, 0.350564, 0.350564), "blue_white": (0.373584, 0.598958, 1), "yellow_lamp": (1, 0.489856, 0.015479)}

point_colors = {"green": (1.0, 0.350564, 0.350564), "yellow_green": (0.394567, 1.0, 0.150458), "yellow": (1.0, 0.819516, 0.057805),
                "purple": (0.854957, 0.358621, 1.0), "white_blue": (0.285345, 0.508991, 1.0), "white": (1.0, 1.0, 1.0)}

shadow_objects = ["coffee cup", "plant"]

THIS_DIR = bpy.path.abspath("//")
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

# Main Class
class ImageGenerator:
    def __init__(self, resolution, draw, light_mood, shadow,camera_ran,rotation_step = 20):
        # Scene information
        self.scene = bpy.data.scenes['Scene']
        self.camera = bpy.data.objects['Camera']
        self.axis = bpy.data.objects['Main Axis']
        self.light_1 = bpy.data.objects['Light_1']
        self.light_2 = bpy.data.objects['Light_2']
        self.receipt = bpy.data.objects['receipt']
        self.coffee_cup = bpy.data.objects['coffee_cup']
        self.coffee_light = bpy.data.objects['coffee_light']
        self.coffee_handler = bpy.data.objects['coffee_handler']
        self.coffee_path = bpy.data.objects['coffee_path']
        self.plant = bpy.data.objects['plant']
        self.plant_light = bpy.data.objects['plant_light']
        self.plant_handler = bpy.data.objects['plant_handler']
        self.plant_path = bpy.data.objects['plant_path']
        self.receipt_handle = bpy.data.objects['receipt handle']
        self.sphere = bpy.data.objects['sphere']
        self.cube = bpy.data.objects['cube']
        self.table_mat = bpy.data.materials["table_background"]
        self.receipt_mat = bpy.data.materials["receipt"]
        self.plant_aloe = bpy.data.materials["plant_aloe"]
        self.aloe_pot = bpy.data.materials["aloe_pot"]
        self.cup_texture = bpy.data.materials["Material"]
        self.world_mat = bpy.data.worlds["World"]
        self.resolution = resolution
        self.draw = draw
        self.light_mood = light_mood
        self.shadow_mode = shadow
        if shadow:
            self.shadow_object = random.choice(shadow_objects)
        # Input your own preferred location for the images and labels
        self.images_filepath = ''
		self.plant_dir = join(THIS_DIR,"plant texture")
		self.cup_dir = join(THIS_DIR,"coffee cup texture")
        self.BackGround_DIR = join(THIS_DIR, "backgrounds")
        self.Environment_DIR = join(THIS_DIR, "environment")
        self.image_width = 0
        self.image_height = 0
        self.camera_rand = camera_ran
        self.rotation_step = rotation_step

    def set_bbs(self, bbs_file):
        # get bbs coords
        bbs_input_path = bbs_file
        bbs_input = open(bbs_input_path, 'r')
        self.bbs_coords = self.get_bbs_input(bbs_input)
        bbs_input.close()

    def set_output_dir_path(self, output_path):
        self.images_filepath = output_path
		
	def load_shadow_object_texture(self):
		if self.shadow_object == 'coffee cup':
			self.cup_texture.node_tree.nodes["Image Texture"].image = bpy.data.images.load(join(self.cup_dir,"Base_color.png"))
			self.cup_texture.node_tree.nodes["Image Texture.001"].image = bpy.data.images.load(join(self.cup_dir,"metallic.png"))
			self.cup_texture.node_tree.nodes["Image Texture.002"].image = bpy.data.images.load(join(self.cup_dir,"roughness.png"))
			self.cup_texture.node_tree.nodes["Image Texture.003"].image = bpy.data.images.load(join(self.cup_dir,"normal.png"))
		else:
			self.plant_aloe.node_tree.nodes["Image Texture"].image  = bpy.data.images.load(join(self.plant_dir,"aloevera_diffure.png"))
			self.plant_aloe.node_tree.nodes["Image Texture.001"].image = bpy.data.images.load(join(self.plant_dir,"aloevera_roughness.png"))
			self.aloe_pot.node_tree.nodes["Image Texture"].image = bpy.data.images.load(join(self.plant_dir,"aloe_pot_basecolor.png"))
			self.aloe_pot.node_tree.nodes["Image Texture.001"].image = bpy.data.images.load(join(self.plant_dir,"aloe_pot_roughness.png"))
			self.aloe_pot.node_tree.nodes["Image Texture.002"].image = bpy.data.images.load(join(self.plant_dir,"aloe_pot_normal.png"))



    def set_scene(self):
        self.hide_shadow_objects()
        if self.shadow_mode:
			self.load_shadow_object_texture()
            self.show_shadow_objects()
            self.set_shadow_object()
        self.select_active_receipt()
        self.reset_modifiers()
        self.set_z_to_floor()
        self.set_render_resolution()
        self.set_camera()
        bpy.context.view_layer.update()

    def set_render_engine(self, engine_name, samples):
        if engine_name == 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.samples = samples
            bpy.context.scene.cycles.device = "GPU"
            bpy.context.scene.cycles.feature_set = "SUPPORTED"
        else:
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    def set_subdivision(self):
        bpy.context.object.modifiers["Subdivision"].levels = 0
        bpy.context.object.modifiers["Subdivision"].render_levels = 0
        bpy.context.object.modifiers["Subdivision.001"].render_levels = 1

    def reset_modifiers(self):
        bpy.context.object.modifiers["SimpleDeform"].angle = 0
        bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'X'
        bpy.context.object.modifiers["Subdivision"].levels = 6
        bpy.context.object.modifiers["Subdivision"].render_levels = 6
        bpy.context.object.modifiers["Subdivision.001"].render_levels = 2
        bpy.context.object.modifiers["Displace"].strength = 0

    def center_receipt_in_cameraview(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["receipt"].select_set(True)
        bpy.ops.view3d.camera_to_view_selected()
        bpy.context.view_layer.update()

    def hide_shadow_objects(self):
        self.coffee_cup.hide_render = True
        self.coffee_light.hide_render = True
        self.plant.hide_render = True
        self.plant_light.hide_render = True

    def show_shadow_objects(self):
        if self.shadow_object == 'coffee cup':
            self.coffee_cup.hide_render = False
            self.coffee_light.hide_render = False
        else:
            self.plant.hide_render = False
            self.plant_light.hide_render = False

    def set_shadow_object(self):
        receipt_edge_x = self.receipt.dimensions[0]
        receipt_edge_y = self.receipt.dimensions[1]
        receipt_radius = max(receipt_edge_x, receipt_edge_y) / 2
        obj_diameter = 0
        if self.shadow_object == 'coffee cup':
            obj_diameter = self.coffee_cup.dimensions[1]
            self.coffee_path.scale[0] = receipt_radius + obj_diameter
            self.coffee_path.scale[1] = receipt_radius + obj_diameter
            self.coffee_path.scale[2] = receipt_radius + obj_diameter
            self.coffee_path.rotation_euler[2] = m.radians(0)
            self.coffee_handler.rotation_euler[2] = m.radians(45)
        else:
            obj_diameter = self.plant.dimensions[0]
            self.plant_path.scale[0] = receipt_radius + obj_diameter
            self.plant_path.scale[1] = receipt_radius + obj_diameter
            self.plant_path.scale[2] = receipt_radius + obj_diameter
            self.plant_path.rotation_euler[2] = m.radians(0)
            self.plant_handler.rotation_euler[2] = m.radians(0)

    def object_lights(self):
        if self.shadow_object == 'coffee cup':
            self.coffee_path.rotation_euler[2] = m.radians(random.randint(0, 361))
            self.coffee_handler.rotation_euler[1] = m.radians(random.randint(-45, 1))
            self.coffee_handler.rotation_euler[2] = m.radians(random.randint(20, 81))
        else:
            self.plant_path.rotation_euler[2] = m.radians(random.randint(0, 361))
            self.plant_handler.rotation_euler[0] = m.radians(random.randint(-70, -55))
            self.plant_handler.rotation_euler[2] = m.radians(random.randint(-110, -70))

    def select_active_receipt(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["receipt"].select_set(True)
        bpy.context.view_layer.objects.active = self.receipt

    def load_document_image(self, img_path):
        path = img_path
        if Path(path).is_file():
            img = bpy.data.images.load(path, check_existing=True)  # Load the image in data
            self.image_width = img.size[0]
            self.image_height = img.size[1]
            self.select_active_receipt()
            # save the ratio for all image sizes
            self.receipt.dimensions.y = self.receipt.dimensions.x * (self.image_height/self.image_width)
            bpy.context.view_layer.update()
            node_tree = self.receipt_mat.node_tree  # Get the current document compositor node tree
            img_comp_node = node_tree.nodes.get('Image Texture')  # Use this if your node already exists
            if img_comp_node:
                img_comp_node.image = img
        else:
            raise Exception(f"The file at {img_path} doesn't exist")

    def set_camera(self):
        self.axis.rotation_euler = (0, 0, 0)
        self.axis.location = (0, 0, 0)
        self.camera.location = (0, 0, 0.5)

    def set_render_resolution(self):
        width, height = self.resolution
        rs = self.scene.render
        rs.resolution_x = width
        rs.resolution_y = height
        bpy.context.view_layer.update()

    def set_z_to_floor(self):
        """ takes an object and gives a z position that puts its bounding box at 0
        """
        bpy.context.view_layer.update()
        bb = self.receipt.bound_box
        lower_pos = (self.receipt.matrix_world @ Vector(bb[0])).z
        diff = self.receipt.matrix_world.translation.z - lower_pos
        self.receipt_handle.location.z = diff + 0.001
        bpy.context.view_layer.update()

    def set_obj_z_to_floor(self, obj,obj_):
        """ takes an object and gives a z position that puts its bounding box at 0
        """
        bpy.context.view_layer.update()
        bb = obj.bound_box
        lower_pos = (obj.matrix_world @ Vector(bb[0])).z
        diff = obj.matrix_world.translation.z - lower_pos
        obj.location.z = diff + 0.001
        bpy.context.view_layer.update()


    def main_rendering_loop(self, level,quantity=50, deform_axis='X'):
        """
        This function represent the main algorithm, it accepts the
        rotation step as input, and outputs the images and the bbs.
        """
        # Define a counter to name each .png and .txt files that are outputted
        render_counter = 0
        while(render_counter < quantity):
            # Define the step with which the pictures are going to be taken
            # Calculate the number of images and labels to generate
            print('Number of renders to create:', quantity)
            if self.draw:
                report_file_path = self.images_filepath + '/progress_report.txt'
                report = open(report_file_path, 'w')
            else:
                report = None
            # Multiply the limits by 10 to adapt to the for loop
            # Define range of heights z in m that the camera is going to pan through
            min_d, max_d = level[1]
            # Define range of beta angles that the camera is going to pan through
            minbeta, maxbeta = level[0]
            # Define range of gamma angles that the camera is going to pan through
            gamma_limits = [0, 360]
            dmin = int(min_d * 10)
            dmax = int(max_d * 10)
            # Refactor the beta limits for them to be in a range from 0 to 360 to adapt the limits to the for loop
            min_beta = (-1) * maxbeta + 90
            max_beta = (-1) * minbeta + 90
            # random camera position mode
            if self.camera_rand:
                # load a random table texture
                self.table_mat.node_tree.nodes["Image Texture"].image = self.load_random_table(self.BackGround_DIR)
                # adjust the ambient brightness of our HDRI world
                self.world_mat.node_tree.nodes["Environment Texture"].image = self.load_random_table(
                    self.Environment_DIR)
                d = random.randint(dmin, dmax)
                self.camera.location = (0, 0, d / 10)
                beta = random.randint(min_beta, max_beta + 1)
                beta_r = (-1) * beta + 90
                gamma = random.randint(gamma_limits[0], gamma_limits[1] + 1)
                render_counter += 1
                axis_rotation = (0, m.radians(beta_r), m.radians(gamma))
                self.axis.rotation_euler = axis_rotation  # Assign rotation to <bpy.data.objects['Empty']> object
                self.synthesize_image(deform_axis, level, render_counter, quantity, d, beta_r, gamma,report)

            # Loop to vary the height of the camera
            else:
                for d in range(dmin, dmax + 1, 5):
                    # Update the height of the camera
                    # Divide the distance z by 10 to re-factor current height
                    if render_counter >= quantity:
                        break
                    self.camera.location = (0, 0, d / 10)


                    # Loop to vary the angle beta
                    for beta in range(min_beta, max_beta + 1, self.rotation_step):
                        if render_counter >= quantity:
                            break
                        beta_r = (-1) * beta + 90

                        # load a random table texture
                        self.table_mat.node_tree.nodes["Image Texture"].image = self.load_random_table(self.BackGround_DIR)

                        # adjust the ambient brightness of our HDRI world
                        self.world_mat.node_tree.nodes["Environment Texture"].image = self.load_random_table(self.Environment_DIR)

                        # Loop to vary the angle gamma 0-360
                        for gamma in range(gamma_limits[0], gamma_limits[1] + 1, self.rotation_step):
                            if render_counter >= quantity:
                                break
                            render_counter += 1
                            # Update the rotation of the axis
                            axis_rotation = (0, m.radians(beta_r), m.radians(gamma))
                            self.axis.rotation_euler = axis_rotation  # Assign rotation to <bpy.data.objects['Empty']> object
                            self.synthesize_image(deform_axis,level,render_counter,quantity,d,beta_r,gamma,report)
        if self.draw:
            report.close()  # Close the .txt file corresponding to the report

    def synthesize_image(self,deform_axis,level,render_counter,quantity,d,beta_r,gamma,report):
        # Bend the Receipt and Displace the surface
        self.bend(deform_axis, level)
        # align document to floor
        self.set_z_to_floor()
        # Configure lighting
        self.set_random_light()
        if self.light_1.data.type != "SUN":
            energy1 = random.randint(3, 18)
            self.light_1.data.energy = energy1
        if self.light_2.data.type != "SUN":
            energy2 = random.randint(1, 15)
            self.light_2.data.energy = energy2
        # check if object mood
        if self.shadow_mode:
            self.object_lights()
        # center cam on receipt
        self.center_receipt_in_cameraview()
        # Generate render
        image_bbs = gen_bbs.render(self.resolution, self.bbs_coords)
        # Take photo of current scene and ouput the render_counter.png file
        self.render_blender(render_counter, image_bbs)
        # Show progress on batch of renders
        if self.draw:
            print('Progress =', str(render_counter) + '/' + str(quantity))
            report.write("On render:" + str(render_counter) + '\n' +
                         "--> Location of the camera:" + '\n' +
                         "     d:" + str(d / 10) + "m" + '\n' +
                         "     Beta:" + str(beta_r) + " Deg" + '\n' +
                         "     Gamma:" + str(gamma) + " Deg" + '\n' +
                         "--> Modifiers Vals:" + '\n' +
                         "    Deform Axis:" + str(self.receipt.modifiers["SimpleDeform"].deform_axis) + '\n' +
                         "     Deform Angle:" + str(self.receipt.modifiers["SimpleDeform"].angle) + " Deg" '\n' +
                         "     Displace Strength" + str(self.receipt.modifiers["Displace"].strength) + " Deg" + '\n' +
                         "--> info of light_1:" + '\n' +
                         "    Type :" + self.light_1.data.type + '\n' +
                         "    Color name :" + self.get_color_name(1) + '\n' +
                         "    energy : " + str(self.light_1.data.energy) + '\n' +
                         "    Location: (x,y,z) = " + str(self.light_1.location) + '\n' +
                         "    Rotation:" + '\n' +
                         "    x:" + str(self.light_1.rotation_euler[0] * 180.0 / m.pi) + "Deg" + ' ' +
                         "    y:" + str(self.light_1.rotation_euler[1] * 180.0 / m.pi) + "Deg" + ' ' +
                         "    z:" + str(self.light_1.rotation_euler[2] * 180.0 / m.pi) + "Deg" + '\n' +
                         "--> info of light_2:" + '\n' +
                         "    Type :" + self.light_2.data.type + '\n' +
                         "    Color name :" + self.get_color_name(2) + '\n' +
                         "    energy : " + str(self.light_2.data.energy) + '\n' +
                         "    Location: (x,y,z) = " + str(self.light_2.location) + '\n' +
                         "    Rotation:" + '\n' +
                         "    x:" + str(self.light_2.rotation_euler[0] * 180.0 / m.pi) + "Deg" + ' ' +
                         "    y:" + str(self.light_2.rotation_euler[1] * 180.0 / m.pi) + "Deg" + ' ' +
                         "    z:" + str(self.light_2.rotation_euler[2] * 180.0 / m.pi) + "Deg" + '\n'
                         )



    def calculate_n_renders(self, rotation_step, level):
        min_d, max_d = level[1]
        min_br, max_br = level[0]
        zmin = int(min_d * 10)
        zmax = int(max_d * 10)

        render_counter = 0

        for d in range(zmin, zmax + 1, 5):
            camera_location = (0, 0, d / 10)
            min_beta = (-1) * max_br + 90
            max_beta = (-1) * min_br + 90

            for beta in range(min_beta, max_beta + 1, rotation_step):
                for gamma in range(0, 361, rotation_step):
                    render_counter += 1

        return render_counter

    def calculate_rot_step(self, quantity, level):
        min_d, max_d = level[1]
        min_br, max_br = level[0]
        zmin = int(min_d * 10)
        zmax = int(max_d * 10)
        min_beta = (-1) * max_br + 90
        max_beta = (-1) * min_br + 90
        diff_d = zmax - zmin + 1
        diff_beta = max_beta - min_beta +1
        diff_gamma = 361
        res = m.ceil(diff_d/5)*m.ceil(diff_gamma/quantity)*diff_beta
        step_rot = m.ceil(m.sqrt(res))
        return step_rot

    def render_blender(self, count_f_name, img_bbs):
        # Render images
        image_name = str(count_f_name) + '.png'
        bbs_file_name = str(count_f_name) + '.json'
        self.scene.render.filepath = self.images_filepath + '/' + image_name
        bbs_file_path = self.images_filepath + '/' + bbs_file_name
        bbs_file = open(bbs_file_path, 'w')
        for word_dict in img_bbs:
            json_string = json.dumps(word_dict)
            bbs_file.write(json_string + '\n')
        bbs_file.close()
        # Take picture of current visible scene
        bpy.ops.render.render(write_still=True)
        # Draw bbs for letters in the current scene
        if self.draw:
            self.draw_bbs(count_f_name, img_bbs)

    def draw_bbs(self, count_f_name, img_bbs):
        image_name = str(count_f_name) + '.png'
        path = self.images_filepath + '/' + image_name
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        for word_dict in img_bbs:
            bb = word_dict['polygon']
            xy = [bb[0], bb[1], bb[1], bb[2], bb[2], bb[3]]
            draw.polygon(xy, outline=(255, 0, 0))
        del draw
        image_name = str(count_f_name) + '_bbs.png'
        path = self.images_filepath + '/' + image_name
        im.save(path)

    def get_bbs_input(self, bbs_input):
        data = json.load(bbs_input)
        letter_bbs_coord = []
        for image_dic in data['images']:
            image_path = image_dic['image_path']
            for word_dic in image_dic['words']:
                name = word_dic['word']
                word_polygon = []
                word_info = {}
                for polygon_dic in word_dic['polygon']:
                    coord = Vector(self.normalize_bb((polygon_dic['x'], polygon_dic['y'])))
                    word_polygon.append(coord)
                word_info['word'] = name
                word_info['polygon'] = word_polygon
                letter_bbs_coord.append(word_info)
        return letter_bbs_coord

    def normalize_bb(self, coord):
        x, y = coord
        x = x / self.image_width
        y = 1 - (y / self.image_height)
        return (x, y)

    def bend(self, deform_axis, level):

        self.receipt.modifiers["SimpleDeform"].deform_method = 'BEND'
        self.receipt.modifiers["SimpleDeform"].origin = self.sphere
        self.receipt.modifiers["SimpleDeform"].deform_axis = deform_axis
        min_angle, max_angle = level[2]
        self.receipt.modifiers["SimpleDeform"].angle = radians(uniform(min_angle, max_angle))
        self.receipt.modifiers["Displace"].texture_coords_object = self.cube
        min_strength, max_strength = level[3]
        self.receipt.modifiers["Displace"].strength = triangular(min_strength, max_strength)

    def load_image(self, path):
        """ load a texture """
        im = bpy.data.images.load(path)
        return im

    def load_table(self, name, dir):
        """ load a table texture """
        path = join(dir, name)
        return self.load_image(path)

    def load_random_table(self, dir):
        """ pick a random table texture and load it"""
        name = random.choice(os.listdir(bpy.path.abspath(dir)))
        return self.load_table(name, dir)

    def set_random_light(self):
        # set random lights types
        light_1 = random.choice(light_types)
        if light_1 == "SUN":
            self.set_sun(1)
        elif light_1 == "POINT":
            self.set_point(1)
        else:
            self.set_spot(1)
        light_2 = random.choice(light_types)
        if light_2 == "SUN":
            self.set_sun(2)
        elif light_1 == "POINT":
            self.set_point(2)
        else:
            self.set_spot(2)
        self.select_active_receipt()

    def set_sun(self, light_id):
        sun = self.light_1
        if light_id == 1:
            self.light_1.data.type = "SUN"
        else:
            self.light_2.data.type = "SUN"
            sun = self.light_2

        sun.data.use_contact_shadow = False
        # pick a random color
        if self.light_mood:
            sun_color = random.choice(list(sun_colors.values()))
        else:
            sun_color = point_colors['white']
        sun.data.color = sun_color
        # set sun energy
        sun.data.energy = random.uniform(0.5, 3)
        # rotation x 0-20 y -10 -30 z 0-360
        x_rotation = random.uniform(0, 20)
        y_rotation = random.uniform(-10, -30)
        z_rotation = random.randint(0, 360)
        sun.rotation_euler[0] = x_rotation * m.pi / 180.0
        sun.rotation_euler[1] = y_rotation * m.pi / 180.0
        sun.rotation_euler[2] = z_rotation * m.pi / 180.0
        # location x -+ 0.6 y+- 0.8 z 0.6-1
        x_location = random.uniform(-0.6, 0.6)
        y_location = random.uniform(-0.8, 0.8)
        z_location = random.uniform(0.6, 1)
        sun.location[0] = x_location
        sun.location[1] = y_location
        sun.location[2] = z_location

    def set_point(self, light_id):
        point = self.light_1
        if light_id == 1:
            self.light_1.data.type = "POINT"
        else:
            self.light_2.data.type = "POINT"
            point = self.light_2

        point.data.use_contact_shadow = False
        if self.light_mood:
            point_color = random.choice(list(point_colors.values()))
        else:
            point_color = point_colors['white']
        point.data.color = point_color
        # for point there is no rotation x(-0.5,0.5) y(+-0.7) z(0.2,0.8)
        x_location = random.uniform(-0.5, 0.5)
        y_location = random.uniform(-0.7, 0.7)
        z_location = random.uniform(0.2, 1)
        point.location[0] = x_location
        point.location[1] = y_location
        point.location[2] = z_location

    def set_spot(self, light_id):
        spot = self.light_1
        if light_id == 1:
            self.light_1.data.type = "SPOT"
        else:
            self.light_2.data.type = "SPOT"
            spot = self.light_2
        spot.data.use_contact_shadow = False
        # pick a random color
        if self.light_mood:
            spot_color = random.choice(list(point_colors.values()))
        else:
            spot_color = point_colors['white']
        spot.data.color = spot_color
        spot.location[0] = 0
        spot.location[1] = 0
        spot.location[2] = 0.5
        # scale the spot
        spot.scale[0] = 0.055
        spot.scale[1] = 0.055
        spot.scale[2] = 0.055
        # rotation x +-7 y -+8 z 0-360
        x_rotation = random.uniform(-7, 7)
        y_rotation = random.uniform(-8, -8)
        z_rotation = random.randint(0, 360)
        spot.rotation_euler[0] = x_rotation * m.pi / 180.0
        spot.rotation_euler[1] = y_rotation * m.pi / 180.0
        spot.rotation_euler[2] = z_rotation * m.pi / 180.0

    def get_color_name(self, light_id):
        light = self.light_1
        if light_id == 2:
            light = self.light_2
        x, y, z = light.data.color
        color = (float("{:.6f}".format(float(x))),float("{:.6f}".format(float(y))), float("{:.6f}".format(float(z))))
        light_type = light.data.type
        if light_type == "SUN":
            return list(sun_colors.keys())[list(sun_colors.values()).index(color)]
        else:
            return list(point_colors.keys())[list(point_colors.values()).index(color)]