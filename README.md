
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

* if it is first time use then we need to install the requirements,to do 
  that in scripting choose install_libs.py then run the script:

  ![setup1](https://user-images.githubusercontent.com/19219983/177786423-431a9e2c-5f96-48ef-a891-49c98e3ca734.png)

  ![setup2](https://user-images.githubusercontent.com/19219983/177786874-18a18f72-0bc6-40fd-a2b6-7bc7b57fa47b.png)

* finally choose SIG.py and run the scrip


#### **Install on Server :**

* First download Blender builder version 3.2.1 or later from :
   
   https://builder.blender.org/download/daily/ 

* Unzip the builder file

* Clone this repository

* open cmd/terminal 

```bash
  cd blender-builder-unziped-folder
```

* In first time use we need to install the required libarys before running, to do that from the 
  cmd/terminal (we opend) run the following command:
```bash
blender path_to_repository/project_v1.2.blend --background --python path_to_repository/install_libs.py
```

* Finally from cmd/terminal (we opend) type this command to run the program :
```bash
blender path_to_repository/project_v1.2.blend --background --python path_to_repository/SIG.py -- path_to_yaml_file
```
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
