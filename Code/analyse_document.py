#---------------------------------------------------------------------------------
#   IADS data science summer school
#   Team: Pink Penguin
#   Company challenge: PROVIDE
#---------------------------------------------------------------------------------
#   The following script converts a pdf to images, and finds text information
#---------------------------------------------------------------------------------

#Import libraries
import pytesseract
#import shutil
import os
#import random
    #try:
#    from PIL import Image
#except ImportError:
#    import Image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
                                  PDFInfoNotInstalledError,
                                  PDFPageCountError,
                                  PDFSyntaxError
                                  )
import cv2
from google.colab.patches import cv2_imshow
import re
from process_text import *


#-------segment file and extract information--------
def processfile(filepath,main_directory):
    
    #temporary path to images
    #temp_directory=main_directory+'Temp_files/'
    temp_directory=main_directory+'Temp_files/'

    #images from pdf
    convert_from_path(filepath,output_folder=temp_directory,output_file='image')

    #make images grayscale
    grayscale = 0
    
    #create empty dictionary to be filled with information from document
    referral_info=create_dict()

    #loop through images (the document)
    n=1
    while True:
        imagename = 'image-'+str(n)+'.ppm'
        if os.path.isfile(temp_directory+imagename):
            
            #read in current image
            img = cv2.imread(temp_directory+imagename, grayscale)
            
            #split image into segments and extract information
            extracted_info=find_boxes(img,referral_info)
        
            #delete processed image file
            os.remove(temp_directory+imagename)
        
            #move to next image/page
            n=n+1
        
        else:
            break

    #save dictionary to csv file
    #data_directory=main_directory+'Database/'
    data_directory=main_directory+'Database/'
    dict_to_csv(extracted_info, data_directory+"storage")

#-------split document into smaller boxes--------
def find_boxes(source_image,referral_info):
    
    #image shape
    image_height, image_width = source_image.shape
    
    #kernels
    kernel_width = 40
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_width, 1))
    kernel_height = 30
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_height))
    
    #amplify horizontal lines
    dilate_image = cv2.dilate(source_image, v_kernel)
    
    # Sum dilated image to 1 column
    v_line_positions = cv2.reduce(dilate_image, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F)
    
    # Normalise the sums back to 255 (8-bit)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(v_line_positions)
    if min_val != max_val:
        v_line_positions -= min_val
        v_line_positions *= 255.0 / (max_val - min_val)

    #split into vertical regions
    previousY = 0
    v_line_threshold = 140
    for y in range(0, image_height):
        if v_line_positions[y] < v_line_threshold:
            if y - previousY > 0:
                if y - previousY > 20:
                    
                    # take the vertical region between the previous and current line positions
                    region = source_image[previousY:y, :]
                    #uncomment to see the regions
                    #cv2_imshow(region)
                    
                    #region shape
                    region_height, region_width = region.shape
                    
                    # amplify vertical lines
                    dilate_region = cv2.dilate(region, h_kernel)

                    # Sum dilated image to 1 row
                    single_row = 0
                    h_line_positions = cv2.reduce(dilate_region, single_row, cv2.REDUCE_SUM, dtype=cv2.CV_64F)
                    h_line_positions /= region_height
                    
                    #split into horizontal regions
                    previousX = 0
                    h_line_threshold = 150
                    for x in range(0, region_width):
                        if h_line_positions[0][x] < h_line_threshold or x == region_width - 1:
                            if x - previousX > 0:
                                if x - previousX > 10:
                
                                    # take the horizontal region between the previous and current line positions
                                    box = region[:, previousX:x]
                                    #uncomment to see the boxes
                                    #cv2_imshow(box)
                
                                    # does the box have text?
                                    box_text = pytesseract.image_to_string(box)
                                    if box_text:
                                        #identify fields and analyse text
                                        referral_info=identify_fields(box_text.strip().lower(),referral_info)
            
                                previousX = x
                
                previousY = y

    return referral_info




