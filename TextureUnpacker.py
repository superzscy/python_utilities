#!/usr/bin/env python
import os
import sys
from PIL import Image
import xml.etree.cElementTree as ET

def frames_from_data(filename):
    frames = []

    tree = ET.ElementTree(file=filename);
    root = tree.getroot()
    for element in tree.iter(tag='image'):
        frame = {}
        frame["name"] = element.attrib['path'][element.attrib['path'].rindex('\\'):];
        frame["x"] = element.attrib['x'];
        frame["w"] = element.attrib['w'];
        frame["y"] = element.attrib['y'];
        frame["h"] = element.attrib['h'];
        frames.append(frame)       
    
    return frames


def gen_png_from_data(filename):
    big_image = Image.open(filename + ".png")
    frames = frames_from_data(filename + ".xml")
    for frame in frames:
        box = (
            int(float(frame['x'])),
            int(float(frame['y'])),
            int(float(frame['x']) + float(frame['w'])),
            int(float(frame['y']) + float(frame['h']))
        )
        rect_on_big = big_image.crop(box)
        rectWidth = int(float(frame['w']))
        rectHeight = int(float(frame['h']))                        
        real_sizelist = [rectWidth, rectHeight]
        result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
        result_box = (
                    int(0),
                    int(0),
                    int(rectWidth),
                    int(rectHeight)
                )
        result_image.paste(rect_on_big, result_box, mask=0)
        #result_image = result_image.transpose(Image.FLIP_TOP_BOTTOM)

        if not os.path.isdir(filename):
            os.mkdir(filename)
        outfile = (filename + '/' + frame['name']).replace('.tex', '.png')
        print(outfile, "generated", rectWidth, rectHeight, box)
        result_image.save(outfile)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("You must pass filename!")
        exit(1)

    filename = sys.argv[1]
    data_filename = filename + ".xml"
    png_filename = filename + '.png'
    if os.path.exists(data_filename) and os.path.exists(png_filename):
        gen_png_from_data(filename)
    else:
        print("Make sure you have both " + data_filename + " and " + png_filename + " files in the same directory")
