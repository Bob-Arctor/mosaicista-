import photos
import numpy as np
from PIL import Image
import math
import evolver

# puck an image from camera roll
target = photos.pick_asset(title='choose a photo', multi=False)

def get_camera_roll():
    albums = photos.get_albums()
    for album in albums:
        print(album.title)
        if album.title == 'Camera Roll':
            return album
    return None
    
    
def make_square(im):
    w = im.size[0]
    h = im.size[1]
    left = 0 if w<=h else int((w-h)/2)
    upper = 0 if w>=h else int((h-w)/2)
    right = w if w<=h else left + h
    lower = h if w>=h else upper + w
    return im.crop((left,upper,right,lower))
    

#make into a square   
shrink = (256, 256)
target = target.get_image()
target = make_square(target)
target = target.resize((shrink[0]*2, shrink[1]*2))
target = target.resize(shrink, Image.ANTIALIAS)
target.show()
print(target.size)
side = target.size[0]

# processing
def pixelate(im, ratio):
    try:
        if im.size[0] != im.size[1]:
            raise ValueError('only square images can be pixelated')
        if ratio <= 0 or ratio > 1:
            raise ValueError('ratio must be between 0 and 1')
    except ValueError as err:
        print(err.args)
        return None
    resized = (int(im.size[0]*ratio),int(im.size[1]*ratio))
    pix = np.array((im.resize(resized)))
    pix = pix.reshape(1,im.size[0]*im.size[1]*3)
    return pix
#    for ibox in xrange(ratio):
#        for jbox in xrange(ratio):
            
length = 5        

t_arr = np.array(target)
t_row = t_arr.reshape(target.size[0] * target.size[1] * 3) 
ratio = 1./length
s_size = target.size
tile_size = (int(s_size[0]*ratio),int(s_size[1]*ratio))


def make_tiled_image(s_size, length, arr=None):
    all_assets = photos.get_assets()
    im = Image.new("RGB", s_size, "white")
    ratio = 1./length
    tile_size = (int(s_size[0]*ratio),int(s_size[1]*ratio))
    tile_size2 = (tile_size[0]*2, tile_size[1]*2)
    for i in xrange(length):
        for j in xrange(length):
            if arr is None:
                a = all_assets[np.random.randint(0,len(all_assets))]
            else:
                a = all_assets[int(arr[i*length+j])]
            a = make_square(a.get_image())
            a = a.resize(tile_size2)
            im.paste(a.resize(tile_size,Image.ANTIALIAS),(i*tile_size[0],j*tile_size[1]))
    return im
        

    
def fit_func(dude):
    tiled = []
    print('estimating fitness for:')
    print(dude)
    length = math.sqrt(len(dude))
    all_assets = photos.get_assets()
    ratio = 1./length
    tile_size = (int(s_size[0]*ratio),int(s_size[1]*ratio))
    for i, pic in enumerate(dude):
        im = make_square(all_assets[pic].get_image())
        im = im.resize((tile_size[0]*2,tile_size[1]*2))
        im = im.resize(tile_size, Image.ANTIALIAS)
        im_arr = np.array(im)
        im_row = im_arr.reshape(im.size[0] * im.size[1] * 3) 
        tiled.extend(im_row)
    tiled = np.array(tiled)
    #print(t_row.shape)
    #print(tiled.shape)
    fitness = np.sum(np.abs(t_row - tiled))
    return fitness
    

all_assets = photos.get_assets()
# number of photo
value_range = [0,len(all_assets)]
# resolution , should be square
length = 8 # 20x20
population = 10
parents = 5
mrate = 0.1

ev = evolver.Evolver(population, parents, mrate, length**2, value_range)
print('curpool:')
print(ev.curpool)

for i in xrange(10):
    ev.evolve(fit_func)
    
print('ev.curfit:')
print(ev.curfit)
print('ev.winners')
print(ev.winners)
print('ev.children')
print(ev.children)
print('ev.curpool')
print(ev.curpool)
print('fittest')
print(ev.fittest)

make_tiled_image(s_size, length, ev.fittest[0]).show()

