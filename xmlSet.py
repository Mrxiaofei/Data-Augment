# encoding: utf-8
import xml.sax
import os

from Transform import *
from scipy.misc import imread
import numpy as np
from PIL import Image
from scipy import misc

class xmlReader(xml.sax.ContentHandler):
    def __init__(self):
        self.contents = {}  # all contents in xml
        # self.tmp = {}  # a piece
        self.backend = 0  # postfix
        self.tag = ''  # name of tag
        self.ParentTag = []  # parent tag
        self.backend_str = []  # follow to store the information of backend
        self.useful_now = False
        self.is_common = ''  # the tag has ended,which may bring error in character()

    def startElement(self, name, attrs):
        self.tag = name  # the name of temporal tag
        self.is_common = ''
        if name == "object":  # object tag in xml
            self.useful_now = True  # objects is in the contents now.
        '''
        self.tmp.clear()#slef.tmp is used for common labels
        self.tmp[name] = ''
        self.contents[self.nodes].setdefault(name)#useless
        '''

    def endElement(self, name):
        if len(self.backend_str):
            name += self.backend_str[-1]
        if name in self.ParentTag:  # just suppose all tag is occured didymous or occured as couple
            self.ParentTag.pop()
            self.backend_str.pop()
        if name == "object":
            self.useful_now = False

        self.tag = name  # the name must equal tag now
        self.is_common = name

    def characters(self, content):
        if self.useful_now:
            # useless information or the tag has been ended
            if len(content) > 0 and content[0] == '\t' or self.is_common == self.tag:
                return

            tmp_dict = self.contents
            for i in self.ParentTag:  # to the last level of the dict of contents
                tmp_dict = tmp_dict[i]

            # obtain a name has no conflict
            key_name = self.tag
            if tmp_dict.get(key_name):
                key_name += str(self.backend)

            if content == '\n':  # at least double connect labels
                tmp_dict[key_name] = {}
                self.ParentTag.append(key_name)  # this is very important
                if key_name == self.tag:
                    self.backend_str.append('')
                else:
                    self.backend_str.append(str(self.backend))
                    self.backend += 1  # all name is different
            else:
                tmp_dict[key_name] = content

    '''
    def __del__(self):
        return  self.contents
    '''


def gotXMLInfo(info):
    # creat XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # defined ContextHandler
    Handler = xmlReader()
    parser.setContentHandler(Handler)

    # read xmlAnno

    parser.parse(info)
    return Handler.contents

def remove_unbox(objects):
    #删除不是boundingbox的信息
    for i in objects.keys():
        if not (type(objects[i]) == dict and objects[i].has_key('bndbox')):
            objects.pop(i)

def mainFunction(image_path, anno_path):
    objects = gotXMLInfo(anno_path) #得到boundingbox的信息
    #print objects
    #for k,v in objects.items():
    #    print k,v
    remove_unbox(objects)
    image = imread(image_path)
#    misc.imsave('save.jpg',image)
    trans_dict = transform(image, objects)
    keys = list(trans_dict.keys())
    #print 'here'
    #print keys
    #print '    ', len(keys)
    idx = random.randint(0, len(keys) - 1)
    return trans_dict[keys[idx]]


def test(xml_path,img_path):
    #info = "/data_1/ssd-project/SSD_data_augment/1_xml/0321_38276453_LSCABN3E4JE276453.xml"
    #photo = "/data_1/ssd-project/SSD_data_augment/1_jpg/0321_38276453_LSCABN3E4JE276453.jpg"
    info = xml_path
    photo = img_path
    #print os.getcwd()
    data, newoj, origin_data = mainFunction(photo, info)
    objects = gotXMLInfo(info)
    '''
    print 'xian zai de label'
    for k,v in newoj.items():
        print k,v
    print 'yuan lai de label'
    objects = gotXMLInfo(info)
    for k,v in objects.items():
        print k,v
        '''
    misc.imsave(photo,data)
    #misc.imsave(photo,data)
    #print '******************'
    #print newoj
    #print '********************'
    return newoj, objects

'''
if __name__ == "__main__":
    test()
'''