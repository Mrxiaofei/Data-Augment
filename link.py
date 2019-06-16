#
import os
from xmlSet import mainFunction
from Transform import *
from scipy.misc import imread


def linkImgAnn(cp):
    data, ann = cp
    dataDir = '/'.join(data.split('/')[0:2])
    annDir = '/'.join(ann.split('/')[0:2])
    extend = '_Aug'


def readFile():
    testFile = '/data_1/ssd-project/SSD_data_augment/data/list.txt'
    for bond in open(testFile):
        #print(bond)
        both = bond.split()
        yield both
        '''
        if os.path.exists(both[0]) and os.path.exists(both[1]) :
            linkImgANN(both)
        '''


def readAnnoImage():

    # read xmlAnno
    couples = readFile()
    xx = (1,)
    for cp in couples:
        try:
            img, anno = cp
            print img,
            if img=='VOC2012/JPEGImages/2009_002851.jpg':
                print 'oo'
            data, labels, origin_data = mainFunction(img, anno)
            tmp = []
            for i in labels.keys():
                tmp.append(labels[i]['name'])
            xx += tuple(tmp)
            # print 'o'
            ###deal with data & its labels
            # show_data(data, labels)
        except Exception, e:
            print 'line:', e
    print xx


if __name__ == "__main__":
    readAnnoImage()
