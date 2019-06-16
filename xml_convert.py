# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:43:01 2019

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
from xmlSet import *
import shutil
def xml_img_copy(xml_path, xml_save_path, img_path, img_save_path):
    imglist=os.listdir(img_path)
    k=0
    for img in imglist:
        name=img
        k=k+1
        print k
        img_datapath=img_path+name
        xml_datapath=xml_path+name.replace("jpg","xml")
        img_name=os.path.splitext(name)
        img_save_name=img_name[0]+'_Augmented'+img_name[1]
        xml_save_name=img_save_name.replace(".jpg",".xml")
        
        img_savepath=img_save_path+img_save_name 
        xml_savepath=xml_save_path+xml_save_name 
        
        #if os.path.exists(img_datapath):
        shutil.copy(img_datapath, img_savepath)
          
        #if os.path.exists(xml_datapath):
        shutil.copy(xml_datapath, xml_savepath)
def xml_modify(xml_path,img_path):
    k=0
    xml_files = os.listdir(xml_path)
    for files in xml_files:
        k= k+1
        print k
        img_files = files.replace(".xml",".jpg")
        print 'cur_img_files:',img_files
        print 'cur_xml_files:',files
        
        newobj, oldobj= test(os.path.join(xml_path,files), os.path.join(img_path,img_files))
        #for i in oldobj:
        #    print i
        #    print oldobj[i]['bndbox']['xmin']
         #   print newobj[i]['bndbox']['xmin']
            
        if not os.path.isdir(files):  
            dom=xml.dom.minidom.parse(os.path.join(xml_path,files))
            root=dom.documentElement
            objects = root.getElementsByTagName("object")
            #print objects
            
            for object_ in objects:
                #xmim
                #xmin_name=object_.getElementsByTagName("xmin")[0].childNodes[0].nodeValue
                name0=object_.getElementsByTagName('xmin')
                n0=name0[0]
                xmin_val=n0.firstChild.data
                #ymin
                #ymin_name=object_.getElementsByTagName("ymin")[0].childNodes[0].nodeValue  
                name1=object_.getElementsByTagName('ymin')
                n1=name1[0]
                ymin_val=n1.firstChild.data
                #xmax
                #xmax_name=object_.getElementsByTagName("xmax")[0].childNodes[0].nodeValue  
                name2=object_.getElementsByTagName('xmax')
                n2=name2[0]
                xmax_val=n2.firstChild.data
                #ymax
                #ymax_name=object_.getElementsByTagName("ymax")[0].childNodes[0].nodeValue
                name3=object_.getElementsByTagName('ymax')
                n3=name3[0]
                ymax_val=n3.firstChild.data
                for i in oldobj:
                    if xmin_val==oldobj[i]['bndbox']['xmin'] and ymin_val==oldobj[i]['bndbox']['ymin'] and xmax_val==oldobj[i]['bndbox']['xmax'] and ymax_val==oldobj[i]['bndbox']['ymax']:
                        n0.firstChild.data=newobj[i]['bndbox']['xmin']
                        n1.firstChild.data=newobj[i]['bndbox']['ymin']
                        n2.firstChild.data=newobj[i]['bndbox']['xmax']
                        n3.firstChild.data=newobj[i]['bndbox']['ymax']
                        print 'find'
            print 'ok!!!',xml_path,files
            with open(os.path.join(xml_path, files), 'w') as fh:
                    dom.writexml(fh)
        dom=xml.dom.minidom.parse(os.path.join(xml_path,files))
        root=dom.documentElement  
        filename1=root.getElementsByTagName('filename')
        n=filename1[0]
        #img_name=os.path.splitext(img_files)
        #name=img_name[0]+'_Augmented'+img_name[1]
        n.firstChild.data=img_files
        size=root.getElementsByTagName('size')
        for i in size:
            width=root.getElementsByTagName('width')
            wid=width[0]
            wid.firstChild.data='300'
            height=root.getElementsByTagName('height')
            hei=height[0]
            hei.firstChild.data='300'
        with open(os.path.join(xml_path, files), 'w') as fh:
            dom.writexml(fh)
                
if __name__ == "__main__":
    img_path = '/data_1/ssd-project/SSD_data_augment/1_jpg/'
    img_save_path = '/data_1/ssd-project/SSD_data_augment/jpg_aug/'
    xml_path = '/data_1/ssd-project/SSD_data_augment/1_xml/'
    xml_save_path = '/data_1/ssd-project/SSD_data_augment/xml_aug/'
    xml_img_copy(xml_path, xml_save_path, img_path, img_save_path)
    xml_modify(xml_save_path,img_save_path)                      