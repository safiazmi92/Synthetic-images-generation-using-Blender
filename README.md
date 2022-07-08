
# Synthetic images generation 

create a synthetic image generator which will be used to train Deep Learning models, in 
the domain of documents understanding. First, we created a 3D scene by projecting 
original 2D document images into 3D meshes. Then we generated 2D images from varying 
camera, light, and background conditions. For this task we used Blender.


## Table of Contents
* [General Information](#general-information)
* [Technologies](#technologies)
* [Features](#features)
* [Screenshots](#screenshots)
* [Demo](#demo)
* [Installation](#installation)
* [Usage](#usage)
* [Project Status](#project-Status)
* [Authors](#authors)
## General Information
- Creat synthetic image generator to make a synthetic labeled text data-set.
- This generator will help in training deep learning models in the domain of documents
  understanding by providing a tool that make thousands of different labeled synthetic
  images from a given labeled image. every image will be taken from different camera 
  angle and have different background, environment,lights colors,lights kind,shape
  and different objects reflecting there shadow.
- We did this project as a part of Industrial project course in our university for IBM 

## Technologies

* Blender 3.2

* Python 3.10 

* Pillow 9.2.0

* PyYAML 6.0


## Features

- Colored Light mode toggle
- Three different light kinds 
- Shadow mode with two object reflecting there shadow
- Draw mode drawing bounding box on output image
- Five different shapes for the output document 


## Screenshots

![4](https://user-images.githubusercontent.com/19219983/176953653-cc905ed1-6902-4c40-980e-662314e87d9d.png)

![8](https://user-images.githubusercontent.com/19219983/176953692-5ef36aa3-d9e2-4555-b70b-f4be02137411.png)

![5_bbs](https://raw.githubusercontent.com/safiazmi92/Synthetic-images-generation-using-Blender/master/outputs/folded_10.jpg/5_bbs.png)

![10_bbs](https://raw.githubusercontent.com/safiazmi92/Synthetic-images-generation-using-Blender/master/outputs/bended_10.jpg/10_bbs.png)

## Demo

- first demo: https://www.youtube.com/watch?v=MNB3RKKlvoA
- second demo: https://www.youtube.com/watch?v=gJC1-iTfwbs



## Installation

There are two options to install:

#### **Running from Blender :** 

* first download Blender version 3.1 or later from:
 
  https://www.blender.org/download/ 

* clone the repository

* open project_v1.2.blend

* To install the dependencies open scripting choose install_libs.py and run the script:

  ![setup1](https://user-images.githubusercontent.com/19219983/177786423-431a9e2c-5f96-48ef-a891-49c98e3ca734.png)

  ![setup2](https://user-images.githubusercontent.com/19219983/177786874-18a18f72-0bc6-40fd-a2b6-7bc7b57fa47b.png)




#### **Install on Server :**

* First download Blender builder version 3.2.1 or later from :
   
   https://builder.blender.org/download/daily/ 

* Unzip the builder file

* Clone this repository

* open cmd/terminal 

```bash
  cd blender-builder-unziped-folder
```

* Install the dependencies before running, to do that from the cmd/terminal (we opend) run the following command:
```bash
  blender path_to_repository/project_v1.2.blend --background --python path_to_repository/install_libs.py
```


## Usage

#### To use on server after completing the installation instruction do the following steps :
* create a yaml file in the following format :
```yaml
input:
  image_path: path_to_origin_image
  
  # Groundtruth is json file contining the bounding box coordinates
  # Of the text on the origin image. see the format at inputs
  groundtruth_path: path_to_groundtruth 
  
output:
  out_dir: path_to_output_folder
  # The number of images to generate
  num_samples: 500
 
 # Choose the shapes of the generated image
 # The quantity of specific shape equals to num_samples*probability. for exampel 
 # In case i don't want flat generated images my probability should be 0 under flat.
 # level is the intensity level of the modifiers on the generated image. There are
 # Three options to choose from : {high,medium,low}.
 # Side is the axi according to it we want to bend/fold the image. There is only
 # Two options to choose from : {X,Z} with capital letters. 
shape:
  flat:
    probability: num 
  bended: 
    level: high/low/medium
    probability: num
    side: X/Z
  wrinkled: 
    level: high/low/medium
    probability: num
  folded: 
    level: high/low/medium
    probability: num
    side: X/Z
  mixed: 
    bend_level:
    bend_side: width/height
    wrinkle_level: 
    probability:
# Render resolution: 1-width_res 2-higth_res. Choose the output resolution as
# It fit your needs. We recommend 1920*1080
render_resolution_1: 1920
render_resolution_2: 1080

# Choose whether you want lights to change their colors or not (False == white color only).  
light_colors: True/False
# choose whether you want to have object reflecting his shadow on the image or not.
object_shadow : True/False
# Choose whether you want to have another image for each generated image with the bounding box
# Drawn upon it to check if output coordinate are correct. by enable this you will
# Get a report file containing all the information about every genterated image.
draw_labels : True/False
# Choose the render engine you want. options are : {BLENDER_EEVEE,CYCLES}
# Cycles is Blender's physically-based path tracer for production rendering.
# Eevee is Blender's realtime render engine built using OpenGL focused on speed
# And interactivity while achieving the goal of rendering PBR materials.
# If you dont have a good GPU we recommend to use eevee in the other case use Cycles.
render_engine : BLENDER_EEVEE/CYCLES
# If you choose Cycles then set the ray tracing sample as it fit yor needs. We 
# recommend 100.
# If you choose eevee it dosnt matter as we dont check this value.  
render_samples : 0
```

* Open cmd/terminal

```bash
  
  cd blender-builder-unziped-folder
  
  #Run the generator
  blender path_to_repository/project_v1.2.blend --background --python path_to_repository/SIG.py -- path_to_yaml_file
```


#### To use from Blender after completing the installation do the following steps:

- Open the SIG.py file with IDE of your choose

- Do the following :
```python
    # Find main function
    if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    with open(argv[0]) as f:
    
    # Comment this lines and add path to your the yaml file
    if __name__ == "__main__":
    # argv = sys.argv
    # argv = argv[argv.index("--") + 1:]
    with open('path_to_yaml_file') as f:     
``` 

- The output generated images and there corresponding bounding box file will be found at the output path specified in the yaml file in both ways.
## Project Status
The project is complete. My plan is to add another features that will be
mainly about rendering the document from objects like phone/pc and other. 
## Authors

Created by:
- [@safiazmi92](https://github.com/safiazmi92)
- [@rahaf698](https://github.com/rahaf698)
feel free to contact us:
- safiazmi92@gmail.com
- rahafhamed97@gmail.com 