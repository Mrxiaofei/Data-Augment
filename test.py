# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:47:51 2019

@author: budefei
"""
import os  
import os.path  
import xml.dom.minidom  
from xml.dom.minidom import parse
import xml.dom.minidom
import os,shutil
import numpy as np
import cv2
from PIL import Image, ImageDraw

path="/data_1/ssd-project/SSD_data_augment/1_xml"  

files=os.listdir(path)
s=[]  
k=0
for xmlFile in files:
    k=k+1
    print k
    print xmlFile
    if not os.path.isdir(xmlFile): 
        #print xmlFile  
        dom=xml.dom.minidom.parse(os.path.join(path,xmlFile))
        root=dom.documentElement  
        objects = root.getElementsByTagName("object")
        for object_ in objects:
            a=object_.getElementsByTagName("name")[0].childNodes[0].nodeValue
            if a=="chebiao11":
                print xmlFile  
                #name=object_.getElementsByTagName('name')
                #n0=name[0]
                #n0.firstChild.data='chebiao11' 
                

                name0=object_.getElementsByTagName('xmin')
                n0=name0[0]
                n0.firstChild.data='121'
                #xmin_val=n0.firstChild.data
                #ymin
                ymin_name=object_.getElementsByTagName("ymin")[0].childNodes[0].nodeValue  
                name1=object_.getElementsByTagName('ymin')
                n1=name1[0]
                #ymin_val=n1.firstChild.data
                #xmax
                xmax_name=object_.getElementsByTagName("xmax")[0].childNodes[0].nodeValue  
                name2=object_.getElementsByTagName('xmax')
                n2=name2[0]
                #xmax_val=n2.firstChild.data
                #ymax
                ymax_name=object_.getElementsByTagName("ymax")[0].childNodes[0].nodeValue
                name3=object_.getElementsByTagName('ymax')
                n3=name3[0]
                ymax_val=n3.firstChild.data
                n3.firstChild.data='11'
        with open(os.path.join(path, xmlFile), 'w') as fh:
            dom.writexml(fh)