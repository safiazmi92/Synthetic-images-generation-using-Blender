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
![1](https://user-images.githubusercontent.com/19219983/175143272-e1548dc8-ce00-404e-9882-4374a8342b21.png)
![1_bbs](https://user-images.githubusercontent.com/19219983/175143329-55e42b85-df8d-43f4-a2da-9efcd4d97f48.png)


