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

fnt_sz = int(hi/4) #-init. max font size
print(fnt_sz)



# draw text; 
fnt = ImageFont.truetype("Freedom-10eM.ttf", fnt_sz)
# min box_sz = 5pt font ~ 20x5 pixels
box_sz = drw.textsize("check", font=fnt) #-get w,h of tex

drw.text((0,0), "check", font = fnt, fill="white")
img.show()
'''


# place images onto canvas


print("\nDONE!")
