# -*- coding: UTF-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def GetAnnotBoxLoc(AnotPath):
    tree = ET.ElementTree(file=AnotPath)
    root = tree.getroot()
    ObjectSet = root.findall('object')
    ObjBndBoxSet = {}
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox = Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)
        cx = (x1+x2)/2
        cy = (y1+y2)/2
        w = x2 - x1
        h = y2 - y1
        BndBoxLoc = [cx, cy, w, h]
        if ObjName in ObjBndBoxSet:
            ObjBndBoxSet[ObjName].append(BndBoxLoc)
        else:
            ObjBndBoxSet[ObjName] = BndBoxLoc
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    return ObjBndBoxSet, width, height


if __name__ == "__main__":
    boundbox = GetAnnotBoxLoc("./label/附件修理翻修报告.xml")
    print(boundbox)
