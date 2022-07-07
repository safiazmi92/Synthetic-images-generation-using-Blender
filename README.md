# Synthetic-images-generation-using-Blender
create a synthetic image generator which will be used to train Deep Learning models, in the domain of documents understanding.
First, we will create a 3D scene by projecting original 2D document images into 3D meshes. Then
we will generate 2D images from varying camera, light, and background conditions. For this task
we will use Blender.
As start we took as input the bounding box of letters then transform them to the 3D scene:
![3](https://user-images.githubusercontent.com/19219983/175209264-c8f81b21-f720-4eaf-811c-5bf125535ccc.png)
Then  the algorithem transform the bounding box to 2D and draw the bounding box:
![3_bbs](https://user-images.githubusercontent.com/19219983/175209291-1e69b56e-bf41-4a14-887a-7a64420c5881.png)
after that we took the bounding box of words in text as input and transform them to the 3D scene: 
![24](https://user-images.githubusercontent.com/19219983/175213277-22bba62b-556d-4bfa-b996-d8f27dbc181e.png)
The algorithm draw the bounding box precisely around every word which indicate that the output coordinate is correct:
![24_bbs](https://user-images.githubusercontent.com/19219983/175213290-5a461b35-9721-45ec-a901-f2a53494e042.png)
Finally we test the algorithm with random input and got the same result.
Random input image                                                                                         | Output image
:---------------------------------------------------------------------------------------------------------:|:--------------------------------------------------:
![1](https://user-images.githubusercontent.com/19219983/175143272-e1548dc8-ce00-404e-9882-4374a8342b21.png) |   ![1_bbs](https://user-images.githubusercontent.com/19219983/175143329-55e42b85-df8d-43f4-a2da-9efcd4d97f48.png)

We added an option to generate images with an object on the scene so we could have shadows on the document: 
![4](https://user-images.githubusercontent.com/19219983/176953653-cc905ed1-6902-4c40-980e-662314e87d9d.png)
![8](https://user-images.githubusercontent.com/19219983/176953692-5ef36aa3-d9e2-4555-b70b-f4be02137411.png)

# Running
There are two options:<br />
### **1- Running from Blender**:

1.1- download Blender from https://www.blender.org/download/ version 3.1 or later

1.2- clone the repository

1.3- open project_v1.2.blend

1.4- go to scripting choose install_libs.py then run the script:<br />
<br />
  1.4.1)<br />
![setup1](https://user-images.githubusercontent.com/19219983/177786423-431a9e2c-5f96-48ef-a891-49c98e3ca734.png)

  1.4.2)<br />
![setup2](https://user-images.githubusercontent.com/19219983/177786874-18a18f72-0bc6-40fd-a2b6-7bc7b57fa47b.png)

1.5- choose SIG.py run the script<br />
<br />
<br />
### **2- Runnig on Server**:

2.1- Download Blender builder from https://builder.blender.org/download/daily/ version 3.2.1 or later

2.2- unzip the builder file

2.3- clone the repository

2.4- open cmd/terminal cd to the Blender builder unziped folder

2.5- if it is first time use then we need to install the requirements,to do that from the cmd/terminal (we opend in 2.4) run the following command:<br />
    blender path_to_repository/project_v1.2.blend --background --python path_to_repository/install_libs.py
    
2.6- from the cmd/terminal (we opend in 2.4) type this command to run the program :<br />
    blender path_to_repository/project_v1.2.blend --background --python path_to_repository/SIG.py -- path_to_yaml_file

