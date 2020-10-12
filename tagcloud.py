'''
algorithm by http://static.mrfeinberg.com/bv_ch03.pdf 

implementation hints by https://github.com/amueller/word_cloud
                        https://github.com/jasondavies/d3-cloud

'''
import numpy as np
import re

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# ~ from PIL import ImageColor
# ~ from PIL import ImageFilter



#---
def normalize_text(s):
    s = s.lower()
    
    # remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    s = re.sub(r'[?()]', '', s)
    
    # make sure we didn't introduce any double spaces
    s = re.sub('\s+',' ',s)
    
    return s
#---


'''
#---
# get tokens from test doc
toks = ""
with open("doin-time.txt", 'r') as t :
	for line in t.readlines() :
		toks = toks + normalize_text(line.rstrip().strip(u'\u200b')) + ' ' 

toks = toks.split()


# remove stop words
cut = []
with open("stopwords.txt", 'r') as s :
	for line in s :
		cut.append(line.rstrip())

payload = []
for word in toks :
	if word not in cut :
		payload.append(word)


# group tokens into n-grams
n = 1
stop_idx = len(payload)-1 - (n-1) #-final n-gram index
grams = []
for i in range(0, stop_idx+1) :
	g = payload[i : i+n]
	grams.append(' '.join(g))
# ~ for g in grams :
	# ~ print(g)


# make frequency dictionary
dct = {}
for g in grams :
	if g not in dct :
		dct.update({g : 1})
	else :
		dct[g] += 1
# ~ for k, v in dct.items() :
	# ~ print(k, ":", v)
	
	
# trim freq dict into ordered list
max_words = 197	
srtd = sorted(dct.items(), key=lambda x : x[1], reverse = True) 

if len(srtd) > max_words :
	srtd = srtd[ :max_words]
# ~ for i in srtd :
	# ~ print(i)	


# scale frequencies to normalized weights in [0,1]
maxw = srtd[0][1]**(1/2) 

for i in range(0, len(srtd)) :
	w = srtd[i][1]**(1/2) / maxw
	srtd[i] = [srtd[i][0], w]
	
for i in srtd :
	print(i)	
	
#---
'''


#---
# create images from weighted tokens
wi = 1000
hi = int(wi/2)
img = Image.new("L", (wi,hi)) #-greyscale canvas
arr = np.asarray(img)
print("size: ", arr.size)
print("dim: ", arr.shape)
print(arr)
'''
drw = ImageDraw.Draw(img) #-get drawing context (pencil)
draw = ImageDraw.Draw(img_grey)
iimg_array = np.asarray(img_grey)

font_sizes, positions, orientations, colors = [], [], [], []
last_freq = 1
max_font_size = 1000

occupancy = IntegralOccupancyMap(height, width, boolean_mask)
if len(srtd) == 1:
# we only have one word. We make it big!
    font_size = 20000
font_size = 10000
random_state = Random()
font_path = ImageFont.truetype("FORTE.ttf")
for word, freq in frequencies:
    if freq==0:
        continue
    #scaling variable
    rs=5
    if rs != 0:
        font_size = int(round((rs * (freq / float(last_freq))+ (1 - rs)) * font_size))
    orientation = Image.ROTATE_90
    tried_other_orientation = False
    while True:
        font = ImageFont.truetype(font_path, font_size)
        transposed_font = ImageFont.TransposedFont(font, orientation=None)
        # get size of resulting text
        box_size = draw.textsize(word, font=transposed_font)    
        result = occupancy.sample_position(box_size[1] + 2,box_size[0] + 2,random_state)
    x, y = np.array(result) + 1
    draw.text((y, x), word, fill="white", font=transposed_font)
    positions.append((x, y))
    orientations.append(orientation)
    colors.append(self.color_func(word, font_size=font_size,position=(x, y),orientation=orientation,random_state=random_state,font_path=self.font_path))font_sizes.append(font_size)
    if self.mask is None:
        img_array = np.asarray(img_grey)
    else:
        img_array = np.asarray(img_grey) + boolean_mask
    # recompute bottom right
    # the order of the cumsum's is important for speed ?!
    occupancy.update(img_array, x, y)
    last_freq = freq

layout  = list(zip(frequencies, font_sizes, positions,
                        orientations, colors))






fnt_sz = int(hi/4) #-init. max font size
print(fnt_sz)



# draw text; 
fnt = ImageFont.truetype("Freedom-10eM.ttf", fnt_sz)
# min box_sz = 5pt font ~ 20x5 pixels
box_sz = drw.textsize("check", font=fnt) #-get w,h of tex

drw.text((0,0), "check", font = fnt, fill="white")
'''


# place images onto canvas


print("\nDONE!")
