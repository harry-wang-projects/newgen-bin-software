import numpy as np
import os
from time import sleep

from classification_specs import IMG_SIZE, number_of_colors 

CATEGORIES = ['Metal', 'Paper', 'Plastic', 'Trash']


def get_pic():

    return CATEGORIES[2]

def verify_classes(name):
    for i in range(10):
        obtained_str = get_pic()
        print("got str: [" +  obtained_str + "], trash: [Trash]")
        if obtained_str == name:
            return True
        sleep(0.2)
    return False



# def get_barcode():

# #    if number_of_colors == 1:
# #        img_array = cv2.imread(1, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
# #    else:
# #        img_array = cv2.imread(1)
#     camera = cv2.VideoCapture(0)
#     return_value, img = camera.read()
#     del(camera)

#     # read the image in numpy array using cv2
#     img = cv2.imread(img)
      
#     # Decode the barcode image
#     detectedBarcodes = decode(img)
            
#     # If not detected then print the message
#     if not detectedBarcodes:
#         print("Barcode Not Detected or your barcode is blank/corrupted!")
#     else:
#           # Traverse through all the detected barcodes in image
#         for barcode in detectedBarcodes: 
                       
#             # Locate the barcode position in image
#             (x, y, w, h) = barcode.rect
                                    
#             # Put the rectangle in image using
#             # cv2 to highlight the barcode
#             cv2.rectangle(img, (x-10, y-10),
#                           (x + w+10, y + h+10),
#                           (255, 0, 0), 2)
                                                 
#             if barcode.data!="":
#                 return barcode.data #student_id

print(get_pic())
