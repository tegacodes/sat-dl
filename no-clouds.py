import os
import glob
import sys
import rasterio
import subprocess
import shutil
import json
from PIL import Image
 

def getTiles(location, satN, start, finish, p, r, lon, lat, tile_path):
    if not os.path.exists(tile_path):
        os.mkdir(tile_path)
    if lat=="0" and lon=="0":
        subprocess.call("landsat -sat "+satN+" --start "+start+" --end "+finish+" --path "+p+" --row "+r+" -o "+tile_path+" --max-cloud-percent 5", shell=True)
    if p=="0" and r=="0":
        subprocess.call("landsat -sat "+satN+" --start "+start+" --end "+finish+" --lat "+lat+" --lon "+lon+" -o "+tile_path+" --max-cloud-percent 5", shell=True)



def combineTiles(tile_path, satN):
    #paths = glob.glob("**/**/*.txt")
    paths = glob.glob(tile_path+"/**/*.txt")


    stackfoldername = tile_path+"-stack"
    if not os.path.exists(stackfoldername):
        os.mkdir(stackfoldername)

    for path in paths:
        lines = open(path).readlines()
        lines = [l.strip() for l in lines]
        cloud_line = [l for l in lines if "CLOUD_COVER = " in l]
        if len(cloud_line) < 1:
            print("NO CLOUD LINE DELETE", os.path.dirname(path))
            shutil.rmtree(os.path.dirname(path))
            continue
        cloud_line = cloud_line[0].split(" = ")
        val = float(cloud_line[1])
        print("VAL", val)
        if val < 10:
            print("KEEPING", path)
            fileN = path.replace("_MTL.txt", "")
            combine_bands2(fileN, stackfoldername, satN)
        else:
            print("DELETE", os.path.dirname(path))
            shutil.rmtree(os.path.dirname(path))
        category = [l for l in lines if "COLLECTION_CATEGORY = " in l]
        if category != "T1":
            print("DELETE", os.path.dirname(path))

            
def combine_bands2(file_, stackfoldername, satN):
    print("Combining bands 2")
    print(stackfoldername)
    print(file_)
    file_name=file_
    # split path
    file_name=file_name.split("/")
    file_name = file_name[-1]
    args = ["bash", "stack.sh", satN, file_+"_B", stackfoldername+"/"+file_name+"_stack.tif"]
    print(" ".join(args))
    subprocess.call(args)


def color_correct(file, satN, folder):
    #convert -sigmoidal-contrast 50x16% RGB.tif RGB-corrected.tif
    #args = ["convert", "-sigmoidal-contrast", "50x16%", file, file+"-corrected.tif"]
    #print(" ".join(args))
    #subprocess.call(args)
    if satN=="8": 
        file_name=file.split(".")
        file_name = file_name[-2]
        print(file_name)
        #args1 = ["convert", "-channel", "B", "-gamma", "0.925", "-channel", "R", "1.03", "-channel", "RGB", "-sigmoidal-contrast", "50x16%", file, file_name+"-corrected.tif"]
        args1 = ["convert", "-channel", "B", "-gamma", "0.925", "-channel", "R", "1.03", "-channel", "RGB", "-sigmoidal-contrast", "50x16%", file, file]
        print(" ".join(args1))
        subprocess.call(args1)
        print("corrected")
    if satN=="88": 
        args2 = ["convert", "-channel", "B", "-gamma", "1.25", "-channel", "G", "gamma", "1.25", "-channel", "RGB", "-sigmoidal-contrast", "15x15%", file, folder+file_name+"-corrected.tif"]
        print(" ".join(args2))
        subprocess.call(args2)
        print("false corrected")


def crop_image(file,location, folder):
    print("Cropping tiles")
    # thumbs="/Users/tegabrain/Documents/PROJECTS/Current/2019-Vienna/sat-tiles/"+location+"-thumbs"
    thumbs=folder+location+"-thumbs"

    print(thumbs)
    if not os.path.exists(thumbs):
        os.mkdir(thumbs)
    im = Image.open(file)
    print(im.size)
    width, height = im.size
    new_width=3*width/5
    new_height=3*height/5
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    im=im.crop((left, top, right, bottom))
    #im=im.resize(int(new_width),int(new_height),Image.ANTIALIAS)
    #im=im.thumbnail((500,500))
    # file=file.split(".")
    # val = file[0]
    #thumbpath = os.path.dirname(file) + location+"thumbs" + os.path.basename(file)
    thumbpath = thumbs + "/" + os.path.basename(file)
    thumbpath = thumbpath.replace(".tif", ".jpg")
    #im.save(thumbs+'/'++"_thumb.jpg", quality=50)
    im.save(thumbpath, quality=50)



if __name__ == "__main__":

    with open("data.json", "r") as read_file:
        mydict = json.load(read_file)

    #print(mydict['cases'][1]['name'])

    for d in mydict['cases']:
        location = d["name"]
        print(location)
        folder=os.getcwd()+"/"
        tile_path=folder+location
        getTiles(location, mydict['satN'], mydict['start'], mydict['finish'], d['path'], d['row'], d['lon'], d['lat'], tile_path)
        combineTiles(tile_path, mydict['satN'])
        for image_file in glob.iglob(tile_path+'-stack/*.tif'):
            color_correct(image_file, mydict['satN'], folder)
            crop_image(image_file, location, folder)
