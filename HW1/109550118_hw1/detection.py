import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    green_color=(0,255,0)#BGR
    red_color=(0,0,255)#BGR
    
    f=open(dataPath,'r')
    #Open detectData.txt file
    for line in f:
    #read each line then stored the data
        filename=line.split()[0]
        path=os.path.join('data/detect',filename)
        #use os.path.join() to combine that it can be a file path
        img=cv2.imread(path)
        faceNum=int(line.split()[1])
        #change the type into int
        for i in range(faceNum):
            data=f.readline()
            x=int(data.split()[0])
            y=int(data.split()[1])
            width=int(data.split()[2])
            height=int(data.split()[3])
            crop_img=img[y:y+height,x:x+width]
            #divide the face image in each image
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            Img=cv2.resize(crop_img,(19,19),interpolation=cv2.INTER_AREA)
            #save the cutting image be grayscale and the size be (19*19)
            if(clf.classify(Img)==1):
            #Use clf.classify to determine whether the cutting image
                cv2.rectangle(img,(x,y),(x+width,y+height),green_color,2)
                #the rectangle line should be green
            else:
                cv2.rectangle(img,(x,y),(x+width,y+height),red_color,2)
                #the rectangle line should be red
        cv2.imshow('image',img)
        #show the original image
        cv2.waitKey(0)

    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
