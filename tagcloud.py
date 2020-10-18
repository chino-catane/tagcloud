import copy as cp
import json
import random
import re

from flask import Flask, jsonify, request, render_template, url_for
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



def a_len(word) :
    '''counts alpha chars in word'''
    n = 0
    for c in word :
        if c.isalpha() is True :
            n += 1
    return n



class TagCloud(object) :

    def __init__(self,wide=850,hi=850,ftype="times.ttf",max_font=100, 
                 min_font=10,ngrams=1,tfile="data.txt",grey=False) :
        '''docstring'''
        self._wide = wide
        self._hi = hi
        self._colors = ['white','red','orange','yellow',
                      'green','blue','indigo','violet']
        self._freqs = []
        self._ftype = ftype
        self._grams = []
        self._grey = grey
        self._layout = []  
        self._lens = []
        self._max_font = max_font
        self._min_font = min_font
        self._ngrams = ngrams
        self._pixel_map = [[-1 for _ in range(self._wide)] 
                         for _ in range(self._hi)]
        self._scalars = []
        self._tfile = tfile

    def normalize_text(self, s) :
        '''docstring'''
        s = s.lower()
        # remove punctuation that is not word-internal 
        # (e.g., hyphens, apostrophes)
        s = re.sub('\s\W',' ',s)
        s = re.sub('\W\s',' ',s)
        s = re.sub(r'[?()]', '', s)
        # make sure we didn't introduce any double spaces
        s = re.sub('\s+',' ',s)
        return s

    def generate_grams(self) : 
        '''docstring'''
        # get tokens from text file
        toks = ""
        with open(self._tfile, 'r') as t :
            for line in t.readlines() :
                line = self.normalize_text(line)
                toks = toks + line.rstrip().strip(u'\u200b') + ' ' 
        toks = toks.split()
        # group tokens into n-grams
        n = self._ngrams
        stop_idx = len(toks)-1 - (n-1) #-final n-gram index
        grams = []
        for i in range(0, stop_idx+1) :
            t = toks[i : i+n]
            grams.append(' '.join(t))        
        # remove stop words
        cut = []
        with open("stopwords.txt", 'r') as s :
            for line in s :
                cut.append(line.rstrip())
        payload = []
        for g in grams :
            if g not in cut :
                payload.append(g)
        # make frequency dictionary
        dct = {} 
        for p in payload :
            if p not in dct :
                dct.update({p : [1, a_len(p)]})
                
            else :
                dct[p][0] += 1
        #        
        srtd = sorted(dct.items(), key=lambda x : x[1], reverse=True)
        # scale frequencies and populate layout lists
        max_freq = srtd[0][1][0]
        for i in srtd :
            freq = i[1][0]
            scalar = freq / max_freq
            self._freqs.append(freq)
            self._scalars.append(scalar)
            self._grams.append(i[0])
            self._lens.append(i[1][1])

    def set_pixels(self, width, height, x, y, k) :
        '''docstring'''
        for i in range(y, y+height+1) :
            if i >= self._hi :
                break 
            for j in range(x, x+width+1) :
                if j >= self._wide :
                    break
                self._pixel_map[i][j] = k 
                
    def set_rpixels(self, width, height, x, y, k):
        for i in range(x, x+height+1) :
            for j in range(y-height, y+1) :
                self._pixel_map[i][j] = k
        return 1

    def check_pixel_map(self, x, y, w, h):
        '''docstring'''
        for i in range(y, y+h):
            for j in range(x ,x+w):
                if self._pixel_map[i][j] != -1 :
                    return 0
        return 1

    def check_rotate(self, x, y, w, h):
        for i in range(x, x+h):
            for j in range(y-w, y):
                if self._pixel_map[i][j] != -1:
                    return 0
        return 1

    def generate_cloud(self) :
        '''docstring'''        
        self.generate_grams()
        #
        if len(self._grams) < 1 :
            print("ERROR: no text")
        # call up a canvas and pen
        img = Image.new('RGB', (self._wide, self._hi))
        draw = ImageDraw.Draw(img)
        # layout first gram
        txt = self._grams[0]
        font_size = self._max_font
        fnt = ImageFont.truetype(self._ftype, font_size)
        (w,h) = draw.textsize(txt, font=fnt)
        x = self._wide//2 - 1 - w//2
        y = self._hi//2 - 1 - h//2
        #
        if self._grey is False : 
            color = random.choice(self._colors)
        else :
            color = self._colors[0]
        #
        # draw first gram
        draw.text((x, y), txt, fill=color, font=fnt)
        # color-in pixel map
        self.set_pixels(w, h, x, y, 0)
        # collect layout info
        conf = {"txt":txt, "freq":self._freqs[0], "len":self._lens[0], 
                "font_size":font_size, "dim":(w,h), 
                "pos":(x,y), "color":color}                 
        self._layout.append(conf)
        # place all other grams
        for i in range(1, len(self._grams)):
            '''docstring'''
            txt = self._grams[i]
            #
            font_size = int(self._scalars[i]*self._max_font)  
            if font_size <= self._min_font:
                font_size = 15
            #
            fnt = ImageFont.truetype(self._ftype, font_size)
            (w,h) = draw.textsize(txt, font=fnt)
            #
            flag = 0
            hit = 0        
            while hit < 1000 and flag is 0 :
                x = random.randint(0, self._wide-1)
                y = random.randint(0, self._hi-1)
                if (x+w) < self._wide and (y+h) < self._hi :
                    flag = self.check_pixel_map(x, y, w, h)
                hit += 1      
            if flag is 1 :
                color = random.choice(self._colors)
                draw.text((x, y), txt, fill=color, font=fnt)
                self.set_pixels(w, h, x, y, i)
                # collect layout info only if placement is successful
                conf = {"txt":txt,"freq":self._freqs[i],
                        "len":self._lens[i],"font_size":font_size,
                        "dim":(w,h),"pos":(x,y),"color":color}                 
                self._layout.append(conf)
        
    def to_image(self) :
        '''docstring'''
        # call up a canvas and pen
        img = Image.new('RGB', (self._wide, self._hi))
        draw = ImageDraw.Draw(img)
        #
        for i in self._layout :
            fnt = ImageFont.truetype(self._ftype, i["font_size"])
            draw.text(i["pos"], i["txt"], i["color"], fnt)
        #
        return img



# generate tag cloud layout
tc = TagCloud(max_font=400, ngrams=1, tfile="jay.txt", grey=False)
tc.generate_cloud()
tc.to_image().show()
# serialize layout 
cdim = json.dumps((tc._wide, tc._hi))
grams = json.dumps(tc._layout)
# Flask
app = Flask(__name__)
#
@app.route('/')
def render() :
    return render_template("root.htm", cdim=cdim, grams=grams)
#
if __name__ == "__main__" :
    #
    app.run(use_reloader=False, debug=True, host="0.0.0.0", port=7777)
