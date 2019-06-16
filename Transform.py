# encoding: utf-8
'''
mirror:probably is 0.5
distort:color jitter
expand:origin image expand to 4*4
crop:random crop
'''
from jaccard import *


# import random
#from PIL import Image, ImageEnhance, ImageOps, ImageFile
#import matplotlib.pyplot as plt
from scipy import misc
# import numpy as np
# import copy

def mirrot_anno(image, objects):
    '''mirror the annoated info at the same time'''
    height, width, channel = image.shape
    coord = ['xmin', 'xmax', 'ymin', 'ymax']
    for i in objects.keys():
        if not (type(objects[i]) == dict and objects[i].has_key('bndbox')):
            continue
        xmin, xmax, ymin, ymax = [int(objects[i]['bndbox'][k]) for k in coord]
        new_xmin = width - xmax
        new_xmax = width - xmin
        objects[i]['bndbox']['xmin'] = new_xmin
        objects[i]['bndbox']['xmax'] = new_xmax


def jitter(data):
    image, min_max = transfer(data)
    image = Image.fromarray(image)
    random_factor = np.random.randint(0, 31) / 10.
    image = ImageEnhance.Color(image).enhance(random_factor)
    random_factor = np.random.randint(5, 11) / 10.
    image = ImageEnhance.Brightness(image).enhance(random_factor)
    random_factor = np.random.randint(10, 21) / 10.
    image = ImageEnhance.Contrast(image).enhance(random_factor)
    '''
    plt.subplot(121)
    plt.imshow(image)
    plt.subplot(122)
    plt.imshow(contrast_image)
    '''
    image = np.array(image)
    image = re_transfer(image, min_max)
    return image


def expand(image, objects, sz, ratio=3):
    """
    zoom out,but be careful:
    if whiter will be applied, the function(whiter) should be carried out after expand()
    ranther than before this function.for matters of Mean_value.
    :param image:
    :param objects:
    :param sz:
    :param ratio:
    :return:
    """
    height, width, channel = image.shape
    aug_sz = (sz[0] * ratio, sz[1] * ratio)
    mean_value = [104, 117, 123]
    # build a canvus
    canvus = np.zeros((aug_sz[0], aug_sz[0], channel), dtype="uint8")
    # canvus_origin = np.zeros((aug_sz[0], aug_sz[0], channel), dtype="uint8")  # origin image for show
    for i in range(channel):
        canvus[:, :, i] = mean_value[i]
        # canvus_origin[:, :, i] = mean_value[i]  # origin image for show

    # insert the image
    h_off = random.randint(0, aug_sz[0] - height)
    w_off = random.randint(0, aug_sz[1] - width)
    canvus[h_off:h_off + height, w_off:w_off + width, :] = image
    # canvus_origin[h_off:h_off + height, w_off:w_off + width, :] = origin_image  # origin image for show
    # adjust the labels
    new_objects = copy.deepcopy(objects)
    coord = ['xmin', 'xmax', 'ymin', 'ymax']
    for i in new_objects.keys():
        if not (type(new_objects[i]) == dict and new_objects[i].has_key('bndbox')):
            continue
        coor = new_objects[i]['bndbox']
        xmin, xmax, ymin, ymax = [int(coor[k]) for k in coord]  # coor's coordination is num now,not a string
        newCoor = [xmin + w_off, xmax + w_off, ymin + h_off, ymax + h_off]
        for k, key in enumerate(coord):
            coor[key] = newCoor[k]

    canvus, new_objects = resize_imgAnno(sz, canvus, new_objects)
    # canvus_origin, _ = resize_imgAnno(sz, canvus_origin, new_objects)
    return [canvus, new_objects]  # , canvus_origin]  # image,lables,origin_image


def whiter(image):
    """
    中心化和标准化处理，得到0均值、标准差为1的服从标准正态分布的数据
    :param image: image.shape=[300,300,3];height,width,channel
    :return: the data after whitering
    """
    im=image.astype('float64')
    data = np.zeros(image.shape).astype('float16')
    w, h, c = image.shape
    for i in range(c):
        data[:, :, i] = (im[:, :, i] - np.mean(im[:, :, i])) / np.std(im[:, :, i])
    return data

def transform(origin_image, objects):
    """
    data augment
    :param origin_image:
    :param objects: annoated dict
    :return:
    """

    # whitening
    image = whiter(origin_image)
    whiter_image = image
    #misc.imsave('save_whiter.jpg',image)
    # image=origin_image
    trans_dict = {}
    objects = objects
    # 1.distort$$
    prob = random.randint(0, 1)
    if prob > 0.5:
        global image
        image = jitter(image)
        print 'distort'
    #trans_dict['distort'] = [image.copy(),copy.deepcopy(objects)]
    
    sz = (300, 300)  # width & height -- order

    # 2.expand image$$

    prob = random.randint(0, 1)
    if prob > 0.5:
        global image
        image, objects = expand(origin_image, objects, sz)
        #misc.imsave('save_expand.jpg',image_expand)
        #print 'expand_label'
        #print lables_expand
        global whiter_image
        whiter_image=whiter(image)
        print 'expand'
     #   trans_dict['expand'] = [whiter_image, objects, image]
    # 3.origin image -- resize$$
    prob = random.randint(1, 2)
    if prob > 0:
        global image
        global whiter_image
        image, objects = resize_imgAnno(sz, whiter_image, objects)
        #misc.imsave('save_resize.jpg',image)
        #print 'resize_label'
        #print objects
        origin_image, _ = resize_imgAnno(sz, origin_image, objects)
        print 'resize'
     #   trans_dict['origin'] = [image.copy(), copy.deepcopy(objects), origin_image.copy()]
    # 4.mirror$$
    prob = random.randint(0, 1)
    if prob > 0.5:
        global image
        image = image[:, ::-1]
        origin_image = origin_image[:, ::-1]
        mirrot_anno(image, objects)
        print 'mirror'
        trans_dict['mirror'] = [image.copy(), copy.deepcopy(objects), origin_image.copy()]
        '''
    # 5.jaccard$$
    try:
        dict_jaccard = corp_image(image, objects, sz, origin_image)
        trans_dict = dict(trans_dict, **dict_jaccard)
        print 'jaccard'
    except Exception, e:
        print "what's wrong:", e
        '''
    trans_dict['mirror'] = [image.copy(), copy.deepcopy(objects), origin_image.copy()]
    return trans_dict
    