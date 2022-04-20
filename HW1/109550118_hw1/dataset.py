import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    dataset=[]
    Path=os.path.join(dataPath,'face')
    #set up the path to reach the folder
    for filename in os.listdir(Path):
    #traverse all images in the folder.
        img_path=os.path.join(Path,filename)
        #combine the path of the image
        img=cv2.imread(img_path , cv2.IMREAD_GRAYSCALE)
        #read the image
        datatuple = (img, 1)
        dataset.append(datatuple)
        #store the data in the array dataset[] as the format datatuple

    Path=os.path.join(dataPath,'non-face')
    for filename in os.listdir(Path):
        img_path=os.path.join(Path,filename)
        img=cv2.imread(img_path , cv2.IMREAD_GRAYSCALE)
        datatuple = (img, 0)
        dataset.append(datatuple)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    return dataset
