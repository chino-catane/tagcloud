import plotly.graph_objs as go
import random
import re

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from textwrap import wrap



class TagCloud(object) :

	def __init__(
		self, wide=850, hi=850, fnt_scalar=100, ftype="times.ttf",
		max_font=100, min_font=10, ngrams=1, tfile="data.txt"
		) :
		
		self.wide = wide
		self.hi = hi
		
		self.colors = ['white','red','orange','yellow',
			'green','blue','indigo','violet']
		self.freq_lst = []
		self.fnt_scalar = fnt_scalar
		self.ftype = ftype
		self.layout = [] #-[grams, fsizes, ftypes, pos, dims, fcolors] 
		self.max_font = max_font
		self.min_font = min_font
		self.ngrams = ngrams
		self.pixel_map = [[-1 for _ in range(self.wide)] for _ in range(self.hi)]
		self.raw_freqs = [] #-bad workaround!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.tfile = tfile


	def normalize_text(self, s):
		s = s.lower()
		
		# remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
		s = re.sub('\s\W',' ',s)
		s = re.sub('\W\s',' ',s)
		s = re.sub(r'[?()]', '', s)
		
		# make sure we didn't introduce any double spaces
		s = re.sub('\s+',' ',s)
		
		return s


	def generate_grams(self) : 
		# get tokens from text file
		toks = ""
		with open(self.tfile, 'r') as t :
			for line in t.readlines() :
				toks = toks + self.normalize_text(line.rstrip().strip(u'\u200b')) + ' ' 

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
		n = self.ngrams
		stop_idx = len(payload)-1 - (n-1) #-final n-gram index
		grams = []
		for i in range(0, stop_idx+1) :
			g = payload[i : i+n]
			grams.append(' '.join(g))


		# make frequency dictionary
		dct = {}
		for g in grams :
			if g not in dct :
				dct.update({g : 1})
			else :
				dct[g] += 1	
			
			
		# sort and scale freq 
		dct = list([key,value] for key,value in dct.items())
		dct.sort(key=lambda x : x[1], reverse=True)
				
		max_freq = dct[0][1]  
	
		for i in range(len(dct)):
			self.raw_freqs.append(dct[i][1]) #-lazy workaround!!!!!!!!!!!!!
			dct[i][1]=int((dct[i][1]*self.fnt_scalar) // max_freq)
			
		self.freq_lst = dct
	

	def set_pixels(self, width, height, x, y, k):
		for i in range(y, y+height+1) :
			if i >= self.hi :
				break 
			for j in range(x, x+width+1) :
				if j >= self.wide :
					break
				self.pixel_map[i][j] = k 


	def check_pixel_map(self, x, y, w, h):
		for i in range(y, y+h):
			for j in range(x ,x+w):
				if self.pixel_map[i][j] != -1 :
					return 0
		return 1		


	def generate_cloud(self) :
		'''
		Returns
		-------
		
		'''
		#self.layout parameters
		grams = []
		fsizes = []
		ftypes = []
		pos = []
		dims = []
		fcolors = []
		
		self.generate_grams()
		
		if len(self.freq_lst) < 1 :
			print("ERROR: no text")

		# layout first gram
		txt = self.freq_lst[0][0]
		font_size = self.freq_lst[0][1]
		fnt = ImageFont.truetype(self.ftype, font_size)
		
		# call up a canvas and pen
		img = Image.new('RGB', (self.wide, self.hi))		
		draw = ImageDraw.Draw(img)		

		(w,h) = draw.textsize(txt, font=fnt)
		x = self.wide//2 - 1 - w//2
		y = self.hi//2 - 1 - h//2
		color = random.choice(self.colors)
		draw.text((x, y), txt, fill=color, font=fnt)
		
		self.set_pixels(w, h, x, y, 0)
		
		# collect layout info
		grams.append(txt) #-layout info
		fsizes.append(font_size) #-layout info
		ftypes.append(fnt) #-layout info
		dims.append((w,h)) #-layout info
		pos.append((x,y)) #-layout info
		fcolors.append(color) #-layout info

		# place all other grams
		for i in range(1, len(self.freq_lst)):
			flag = 0
			txt = self.freq_lst[i][0]
			
			font_size = int((self.freq_lst[i][1]*100) / self.max_font)  
			if font_size <= self.min_font:
				font_size = 15
			
			fnt = ImageFont.truetype(self.ftype, font_size)
			(w,h) = draw.textsize(txt, font=fnt)
			
			hit = 0
			# vertical layouts
		# ~ if i==2 or i==5 or i==7 or i==10 or i==20 or i==50 or i==80 or i==100 :
			# ~ fnt = ImageFont.TransposedFont(fnt, orientation=Image.ROTATE_90)
			# ~ while flag != 1 :
				# ~ x_coordinate,y_coordinate = get_x_and_y(0,X,Y)
				# ~ if (x_coordinate+h)<X and (y_coordinate+w)<Y :
					# ~ flag = check_if_possible_rotate(pixels, x_coordinate, y_coordinate, h, w)
				# ~ if hit > 1000:
					# ~ break
				# ~ hit += 1
			# ~ draw.text((x_coordinate, y_coordinate),txt,fill=generate_random_color() ,font=fnt)
			# ~ pixels=set_pixels_rotate(pixels,h,w,x_coordinate, y_coordinate,i)
			# ~ continue
        
			while flag != 1 :
				x = random.randint(0, self.wide-1)
				y = random.randint(0, self.hi-1)
				if (x+w)<self.wide and (y+h)<self.hi :
					flag = self.check_pixel_map(x, y, w, h)

				if hit > 1000:
					break
				hit += 1      
    
			if flag is 1 :
				color = random.choice(self.colors)
				draw.text((x, y), txt, fill=color, font=fnt)
				self.set_pixels(w, h, x, y, i)
				
				# collect layout info only if placement is successful
				grams.append(txt) #-layout info
				fsizes.append(font_size) #-layout info
				ftypes.append(fnt) #-layout info
				dims.append((w,h)) #-layout info
				pos.append((x,y)) #-layout info
				fcolors.append(color) #-layout info	
	
		self.layout = list(zip(grams, self.raw_freqs, fsizes, 
			ftypes, dims, pos, fcolors))

	def print_layout(self) :
		for l in self.layout :
			print(l)
		print("\n\n")	


	def to_image(self) :
		# call up a canvas and pen
		img = Image.new('RGB', (self.wide, self.hi))		
		draw = ImageDraw.Draw(img)	
		#-[grams, fsizes, ftypes, pos, dims, fcolors] 
		for (txt, freqs, size, fnt, (width, height), (x,y), color) in self.layout :
			draw.text((x, y), txt, fill=color, font=fnt)
		
		return img
		

'''
GRAVEYARD
---------

if __name__ == "__main__" :
	tc = TagCloud(fnt_scalar=150, ngrams=1, tfile="doin-time.txt")
	tc.generate_cloud()
	tc.print_freq_lst()	

	print("\nDONE!")

'''
