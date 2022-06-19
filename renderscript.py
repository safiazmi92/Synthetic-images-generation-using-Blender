## Import all relevant libraries
import bpy
import os
import sys
from os.path import join
import numpy as np
import math as m
import random
import json
from math import radians
from mathutils import Vector
from random import uniform , triangular
from PIL import Image, ImageDraw
gen_bbs = bpy.data.texts["gen_bbs"].as_module()


## Main Class
class Render:
    def __init__(self):
        ## Scene information
        # Define the scene information
        self.scene = bpy.data.scenes['Scene']
        # Define the information relevant to the <bpy.data.objects>
        self.camera = bpy.data.objects['Camera']
        self.axis = bpy.data.objects['Main Axis']
        self.light_1 = bpy.data.objects['Light_1']
        self.light_2 = bpy.data.objects['Light_2']
        self.recept = bpy.data.objects['receipt']
        self.sphere = bpy.data.objects['sphere']
        self.cube = bpy.data.objects['cube']
        self.table_mat = bpy.data.materials["tablebackground"]
        self.world_mat = bpy.data.worlds["World"]
        
        
        ## Render information
        # Define range of heights z in m that the camera is going to pan through
        self.camera_d_limits = [0.5, 1]
        # Define range of beta angles that the camera is going to pan through
        self.beta_limits = [60, -60]
        # Define range of gamma angles that the camera is going to pan through
        self.gamma_limits = [0, 360] 
        
        ## Output information
        # Input your own preferred location for the images and labels
        self.project_path = 'C:\\Users\\safi_\\Desktop\\project\\'
        self.images_filepath ='C:\\Users\\safi_\\Desktop\\project\\outputs'
        self.BackGround_DIR = 'C:\\Users\\safi_\\Desktop\\project\\backgrounds'
        self.Environment_DIR = 'C:\\Users\\safi_\\Desktop\\project\\enviroment'
        
    def set_camera(self):
        self.axis.rotation_euler = (0, 0, 0)
        self.axis.location = (0, 0, 0)
        self.camera.location = (0, 0, 0.5)
        
    def main_rendering_loop(self, rot_step):
        '''
        This function represent the main algorithm explained in the Tutorial, it accepts the
        rotation step as input, and outputs the images and the labels to the above specified locations.
        '''
        ## Calculate the number of images and labels to generate
        n_renders = self.calculate_n_renders(rot_step) # Calculate number of images
        print('Number of renders to create:', n_renders) 
        
        accept_render = input('\nContinue?[Y/N]:  ') # Ask whether to procede with the data generation

        if accept_render == 'Y': # If the user inputs 'Y' then procede with the data generation
            # Create .txt file that record the progress of the data generation
            report_file_path = self.images_filepath + '/progress_report.txt'
            report = open(report_file_path, 'w')
            bbs_input_path = self.project_path + '/input_bbs.json'
            bbs_input = open(bbs_input_path,'r')
            bbs_coords = self.get_bbs_input(bbs_input)
            bbs_input.close()
            # Multiply the limits by 10 to adapt to the for loop
            dmin = int(self.camera_d_limits[0] * 10)
            dmax = int(self.camera_d_limits[1] * 10)
            # Define a counter to name each .png and .txt files that are outputted
            render_counter = 0
            # Define the step with which the pictures are going to be taken
            rotation_step = rot_step
            for d in range(dmin, dmax + 1, 2): # Loop to vary the height of the camera
                ## Update the height of the camera
                # Divide the distance z by 10 to re-factor current heigh   
                self.camera.location = (0, 0, d/10)
                
                # Refactor the beta limits for them to be in a range from 0 to 360 to adapt the limits to the for loop
                min_beta = (-1)*self.beta_limits[0] + 90
                max_beta = (-1)*self.beta_limits[1] + 90
                
                for beta in range(min_beta, max_beta + 1, rotation_step): # Loop to vary the angle beta
                    beta_r = (-1)*beta + 90 # Re-factor the current beta
                    
                    # load a random table texture
                    self.table_mat.node_tree.nodes["Image Texture"].image = self.load_random_table(self.BackGround_DIR)

                    # adjust the ambient brightness of our HDRI world
                    self.world_mat.node_tree.nodes["Environment Texture"].image = self.load_random_table(self.Environment_DIR)
    
                    for gamma in range(self.gamma_limits[0], self.gamma_limits[1] + 1, rotation_step): # Loop to vary the angle gamma
                        render_counter += 1 # Update counter
                        
                        ## Update the rotation of the axis
                        axis_rotation = (0, m.radians(beta_r), m.radians(gamma)) 
                        self.axis.rotation_euler = axis_rotation # Assign rotation to <bpy.data.objects['Empty']> object
                        # Bend the Receipt and Displace the surface
                        self.bend()
                        # Display demo information - Location of the camera
                        print("On render:", render_counter)
                        print("--> Location of the camera:")
                        print("     d:", d/10, "m")
                        print("     Beta:", str(beta_r)+" Deg")
                        print("     Gamma:", str(gamma)+" Deg")
                        print("--> Modifiers Vals:")
                        print("    Deform Axis:",str(self.recept.modifiers["SimpleDeform"].deform_axis))
                        print("     Deform Angle:", str(self.recept.modifiers["SimpleDeform"].angle)+" Deg")
                        print("     Displace Strenght", str(self.recept.modifiers["Displace"].strength)+" Deg")
                        
                        
                        ## Configure lighting
                        energy1 = random.randint(0, 30) # Grab random light intensity
                        self.light_1.data.energy = energy1 # Update the <bpy.data.objects['Light']> energy information
                        energy2 = random.randint(4, 20) # Grab random light intensity
                        self.light_2.data.energy = energy2 # Update the <bpy.data.objects['Light2']> energy information
                        
                        
                        ## Generate render
                        image_bbs=gen_bbs.render((1920,1080),bbs_coords)
                        self.render_blender(render_counter,image_bbs) # Take photo of current scene and ouput the render_counter.png file
                        
                        ## Show progress on batch of renders
                        print('Progress =', str(render_counter) + '/' + str(n_renders))
                        report.write('Progress: ' + str(render_counter) + ' Rotation: ' + str(axis_rotation) + ' z_d: ' + str(d / 10) + '\n')

            report.close() # Close the .txt file corresponding to the report

        else: # If the user inputs anything else, then abort the data generation
            print('Aborted rendering operation')
            pass
        
    def calculate_n_renders(self, rotation_step):
        zmin = int(self.camera_d_limits[0] * 10)
        zmax = int(self.camera_d_limits[1] * 10)

        render_counter = 0
        rotation_step = rotation_step

        for d in range(zmin, zmax+1, 2):
            camera_location = (0,0,d/10)
            min_beta = (-1)*self.beta_limits[0] + 90
            max_beta = (-1)*self.beta_limits[1] + 90

            for beta in range(min_beta, max_beta+1,rotation_step):
                beta_r = 90 - beta

                for gamma in range(self.gamma_limits[0], self.gamma_limits[1]+1,rotation_step):
                    render_counter += 1
                    axis_rotation = (beta_r, 0, gamma)

        return render_counter
    
    def render_blender(self, count_f_name,img_bbs):
        # Render images
        image_name = str(count_f_name) + '.png'
        bbs_file_name = str(count_f_name) + '.txt'
        self.scene.render.filepath =  self.images_filepath + '/' + image_name
        bbs_file_path = self.images_filepath + '/' + bbs_file_name
        bbs_file = open(bbs_file_path, 'w')
        for bb in img_bbs:
            bbs_file.write('Position ul: ' + str(bb[0]) + ' Position ur: ' + str(bb[1]) + 'Position br: ' + str(bb[2])
         + ' Position bl: ' + str(bb[3]) + '\n')
        bbs_file.close()
        # Take picture of current visible scene
        bpy.ops.render.render(write_still=True)
        # Draw bbs for letters in the current scene
        self.draw_bbs(count_f_name,img_bbs)
        
    def draw_bbs(self,count_f_name,img_bbs):
        image_name = str(count_f_name)+'.png'
        path = self.images_filepath + '/' + image_name
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        #tlx,tly = ul
        #brx,bry= br     
        #trx = brx
        #_try = tly
        #blx = tlx
        #bly = bry
        #draw.rectangle((bl,ur),outline= (255, 0, 0))
        for bb in img_bbs:
            xy = [bb[0],bb[1],bb[1],bb[2],bb[2],bb[3]]
            draw.polygon(xy,outline= (255, 0, 0))
        del draw
        image_name = str(count_f_name)+'_bbs.png'
        path = self.images_filepath + '/' + image_name
        im.save(path)
        
    def get_bbs_input(self,bbs_input):
        data = json.load(bbs_input)
        letter_bbs_coord = []
        for dic in data['bbs_coords']:
            #print(dic)
            #print(dic.items())
            coords = dic.values()
            coord=list(coords)[0]
            print(coord)
            #letter,coord = dic.items()
            for i in range(0,len(coord),4):
                ul = Vector(self.normalize_bb((coord[i],coord[i+1])))
                ur = Vector(self.normalize_bb((coord[i+2], coord[i+1])))
                br = Vector(self.normalize_bb((coord[i+2], coord[i+3])))
                bl = Vector(self.normalize_bb((coord[i], coord[i+3])))
                letter_bbs_coord.append([ul, ur, br, bl])
        return letter_bbs_coord
    
    def normalize_bb(slef,coord):
        x,y =coord
        x = x/1024
        y = 1-(y/512)
        return (x,y)
    
    def bend(self):
    #cuts_ran = random.randint(10,30)
    #fractal_ran = random.uniform(0,0.15)
        self.recept.modifiers["SimpleDeform"].deform_method = 'BEND'
        self.recept.modifiers["SimpleDeform"].origin = self.sphere
        random_num = random.randint(1,2)
        if random_num == 1:
            self.recept.modifiers["SimpleDeform"].deform_axis = 'X'
        else:
            self.recept.modifiers["SimpleDeform"].deform_axis = 'Z'
            
        self.recept.modifiers["SimpleDeform"].angle = radians(uniform(-5.5, 90))
        self.recept.modifiers["Displace"].texture_coords_object = self.cube
        self.recept.modifiers["Displace"].strength = triangular(-0.2, 0.3) 
    
    def load_image(self,path):
        """ load a texture """
        im = bpy.data.images.load(path)
        return im

    def load_table(self,name,dir):
        """ load a table texture """
        path = join(dir, name)
        return self.load_image(path)

    def load_random_table(self,dir):
        """ pick a random table texture and load it"""
        name = random.choice(os.listdir(bpy.path.abspath(dir)))
        return self.load_table(name,dir)
    
    
    ## Run data generation
if __name__ == '__main__':
    # Initialize rendering class as r
    r = Render()
    # Initialize camera
    r.set_camera()
    # Begin data generation
    rotation_step = 70
    r.main_rendering_loop(rotation_step)

#for k in bpy.data.worlds["World"].node_tree.nodes:
#    print (k)