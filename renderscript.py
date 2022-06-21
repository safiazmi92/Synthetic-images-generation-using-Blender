## Import all relevant libraries
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


## Main Class
class ImageGenerator:
    def __init__(self, resolution):
        # # Scene information
        # Define the scene information
        self.scene = bpy.data.scenes['Scene']
        # Define the information relevant to the <bpy.data.objects>
        self.camera = bpy.data.objects['Camera']
        self.axis = bpy.data.objects['Main Axis']
        self.light_1 = bpy.data.objects['Light_1']
        self.light_2 = bpy.data.objects['Light_2']
        self.receipt = bpy.data.objects['receipt']
        self.receipt_handle = bpy.data.objects['receipt handle']
        self.sphere = bpy.data.objects['sphere']
        self.cube = bpy.data.objects['cube']
        self.table_mat = bpy.data.materials["table_background"]
        self.receipt_mat = bpy.data.materials["receipt"]
        self.world_mat = bpy.data.worlds["World"]
        self.resolution = resolution
        # set document image
        # check bbs path
        # set render resolution
        # Render information
        # Output information
        # Input your own preferred location for the images and labels
        self.project_path = 'C:\\Users\\safi_\\Desktop\\project\\inputs'
        self.images_filepath = 'C:\\Users\\safi_\\Desktop\\project\\outputs'
        self.BackGround_DIR = 'C:\\Users\\safi_\\Desktop\\project\\backgrounds'
        self.Environment_DIR = 'C:\\Users\\safi_\\Desktop\\project\\enviroment'

    def set_scene(self, img_path):
        self.load_document_image(img_path)
        self.set_render_resolution()
        self.reset_modifiers()
        self.set_camera()
        self.set_z_to_floor()
        bpy.context.view_layer.update()

    def reset_modifiers(self):
        bpy.context.object.modifiers["SimpleDeform"].angle = 0
        bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'X'
        bpy.context.object.modifiers["Subdivision"].levels = 6
        bpy.context.object.modifiers["Subdivision"].render_levels = 6
        bpy.context.object.modifiers["Displace"].strength = 0

    def load_document_image(self, img_path):
        path = img_path
        if Path(path).is_file():
            img = bpy.data.images.load(path, check_existing=True)  # Load the image in data
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

    def main_rendering_loop(self, bbs_file, deform_axis, level, light_mod, quantity):
        '''
        This function represent the main algorithm explained in the Tutorial, it accepts the
        rotation step as input, and outputs the images and the labels to the above specified locations.
        '''
        ## Calculate the number of images and labels to generate
        n_renders = self.calculate_n_renders(quantity, level)  # Calculate number of images need to work on ti
        print('Number of renders to create:', n_renders)

        accept_render = input('\nContinue?[Y/N]:  ')  # Ask whether to procede with the data generation will remove after finishing
        if accept_render == 'Y':  # If the user inputs 'Y' then procede with the data generation
            # Create .txt file that record the progress of the data generation
            report_file_path = self.images_filepath + '/progress_report.txt'
            report = open(report_file_path, 'w')
            bbs_input_path = bbs_file
            bbs_input = open(bbs_input_path, 'r')
            bbs_coords = self.get_bbs_input(bbs_input)
            bbs_input.close()
            # Multiply the limits by 10 to adapt to the for loop
            # Define range of heights z in m that the camera is going to pan through
            min_d, max_d = level[1]
            # Define range of beta angles that the camera is going to pan through
            minbeta, maxbeta = level[0]
            # Define range of gamma angles that the camera is going to pan through
            gamma_limits = [0, 360]
            dmin = int(min_d * 10)
            dmax = int(max_d * 10)
            # Define a counter to name each .png and .txt files that are outputted
            render_counter = 0
            # Define the step with which the pictures are going to be taken
            rotation_step = quantity
            for d in range(dmin, dmax + 1, 5):  # Loop to vary the height of the camera
                # Update the height of the camera
                # Divide the distance z by 10 to re-factor current height
                self.camera.location = (0, 0, d / 10)  # 0.5,0.7,0.9

                # Refactor the beta limits for them to be in a range from 0 to 360 to adapt the limits to the for loop
                min_beta = (-1) * maxbeta + 90
                max_beta = (-1) * minbeta + 90

                for beta in range(min_beta, max_beta + 1, rotation_step):  # Loop to vary the angle beta
                    beta_r = (-1) * beta + 90  # Re-factor the current beta 60 -60

                    # load a random table texture
                    self.table_mat.node_tree.nodes["Image Texture"].image = self.load_random_table(self.BackGround_DIR)

                    # adjust the ambient brightness of our HDRI world
                    self.world_mat.node_tree.nodes["Environment Texture"].image = self.load_random_table(self.Environment_DIR)

                    for gamma in range(gamma_limits[0], gamma_limits[1] + 1, rotation_step):  # Loop to vary the angle gamma 0-360
                        render_counter += 1  # Update counter

                        # Update the rotation of the axis
                        axis_rotation = (0, m.radians(beta_r), m.radians(gamma))
                        self.axis.rotation_euler = axis_rotation  # Assign rotation to <bpy.data.objects['Empty']> object
                        # Bend the Receipt and Displace the surface
                        self.bend(deform_axis, level)
                        self.set_z_to_floor()
                        # Display demo information - Location of the camera
                        print("On render:", render_counter)
                        print("--> Location of the camera:")
                        print("     d:", d / 10, "m")
                        print("     Beta:", str(beta_r) + " Deg")
                        print("     Gamma:", str(gamma) + " Deg")
                        print("--> Modifiers Vals:")
                        print("    Deform Axis:", str(self.receipt.modifiers["SimpleDeform"].deform_axis))
                        print("     Deform Angle:", str(self.receipt.modifiers["SimpleDeform"].angle) + " Deg")
                        print("     Displace Strength", str(self.receipt.modifiers["Displace"].strength) + " Deg")

                        # Configure lighting
                        min_energy, max_energy = light_mod
                        energy1 = random.randint(min_energy, max_energy)  # Grab random light intensity
                        self.light_1.data.energy = energy1  # Update the <bpy.data.objects['Light']> energy information
                        energy2 = random.randint(min_energy, max_energy)  # Grab random light intensity
                        self.light_2.data.energy = energy2  # Update the <bpy.data.objects['Light2']> energy information

                        # Generate render
                        image_bbs = gen_bbs.render(self.resolution, bbs_coords)
                        self.render_blender(render_counter, image_bbs)  # Take photo of current scene and ouput the render_counter.png file

                        ## Show progress on batch of renders
                        print('Progress =', str(render_counter) + '/' + str(n_renders))
                        report.write(
                            'Progress: ' + str(render_counter) + ' Rotation: ' + str(axis_rotation) + ' z_d: ' + str(d / 10) + '\n')

            report.close()  # Close the .txt file corresponding to the report

        else:  # If the user inputs anything else, then abort the data generation
            print('Aborted rendering operation')
            pass

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

    def render_blender(self, count_f_name, img_bbs):
        # Render images
        image_name = str(count_f_name) + '.png'
        bbs_file_name = str(count_f_name) + '.txt'
        self.scene.render.filepath = self.images_filepath + '/' + image_name
        bbs_file_path = self.images_filepath + '/' + bbs_file_name
        bbs_file = open(bbs_file_path, 'w')
        for bb in img_bbs:
            bbs_file.write('Position ul: ' + str(bb[0]) + ' Position ur: ' + str(bb[1]) + 'Position br: ' + str(bb[2])
                           + ' Position bl: ' + str(bb[3]) + '\n')
        bbs_file.close()
        # Take picture of current visible scene
        bpy.ops.render.render(write_still=True)
        # Draw bbs for letters in the current scene
        self.draw_bbs(count_f_name, img_bbs)

    def draw_bbs(self, count_f_name, img_bbs):
        image_name = str(count_f_name) + '.png'
        path = self.images_filepath + '/' + image_name
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        for bb in img_bbs:
            xy = [bb[0], bb[1], bb[1], bb[2], bb[2], bb[3]]
            draw.polygon(xy, outline=(255, 0, 0))
        del draw
        image_name = str(count_f_name) + '_bbs.png'
        path = self.images_filepath + '/' + image_name
        im.save(path)

    def get_bbs_input(self, bbs_input):
        data = json.load(bbs_input)
        letter_bbs_coord = []
        for dic in data['bbs_coords']:
            coords = dic.values()
            coord = list(coords)[0]
            print(coord)
            for i in range(0, len(coord), 4):
                ul = Vector(self.normalize_bb((coord[i], coord[i + 1])))
                ur = Vector(self.normalize_bb((coord[i + 2], coord[i + 1])))
                br = Vector(self.normalize_bb((coord[i + 2], coord[i + 3])))
                bl = Vector(self.normalize_bb((coord[i], coord[i + 3])))
                letter_bbs_coord.append([ul, ur, br, bl])
        return letter_bbs_coord

    def normalize_bb(slef, coord):
        x, y = coord
        x = x / 1024
        y = 1 - (y / 512)
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

    ## Run data generation


if __name__ == '__main__':
    # Initialize rendering class as r
    r = ImageGenerator()
    # Initialize camera
    r.set_camera()
    # Begin data generation
    rotation_step = 70
    r.main_rendering_loop(rotation_step)

# for k in bpy.data.worlds["World"].node_tree.nodes:
#    print (k)
