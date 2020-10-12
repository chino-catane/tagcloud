import re
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from textwrap import wrap
import random

#To check if pixels are available
def check_if_possible(pixels,x_coordinate,y_coordinate,w,h):
    for i in range(y_coordinate,y_coordinate+h):
        for j in range(x_coordinate,x_coordinate+w):
            if pixels[i][j]==1:
                return 0
    return 1
            

#set the used pixels
def generate_random_color():
    color=['blue','magenta','yellow','black','white','pink']
    return random.choice(color)
    
def set_pixels(pixels,width,height,X,Y):
    for i in range(Y,Y+height+1):
        for j in range(X,X+width+1):
            pixels[i][j]=1
    return pixels

#generate random x and y co-ordinates
def get_x_and_y(mini,X,Y):
    x=random.randint(0,X-1)
    y=random.randint(0,Y-1)
    return (x,y)

#get width and height of the word
def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

#Remove the unnecessary content
def normalize_text(s):
    s = s.lower()
    
    # remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    s = re.sub(r'[?()]', '', s)
    
    # make sure we didn't introduce any double spaces
    s = re.sub('\s+',' ',s)
    
    return s

# get tokens from test doc
toks = ""
with open("data.txt", 'r') as t :
    for line in t.readlines() :
        toks = toks + normalize_text(line.rstrip().strip(u'\u200b')) + ' ' 

toks = toks.split()

#checking for garbage letters and characters
toks1=[]
for i in toks:
    if i.isalpha():
        toks1.append(i)
toks=toks1

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


# make frequency dictionary
dct = {}
for g in grams :
    if g not in dct :
        dct.update({g : 1})
    else :
        dct[g] += 1
dct=list([key,value] for key,value in dct.items())
dct.sort(key=lambda x:x[1],reverse=True)
maximum=dct[0][1]
for i in range(len(dct)):
    dct[i][1]=int((dct[i][1]*100)//maximum)




#WordCloud
if len(dct)<1:
    print("Enter a text with atleast one word")
X=800
Y=800
pixels=[[0 for _ in range(X)]for _ in range(Y)]
txt=dct[0][0]
font_size=dct[0][1]
fnt = ImageFont.truetype("times.ttf",font_size)
w,h=get_text_dimensions(txt, fnt)
img = Image.new('RGB', (X, Y), color = 'cyan')
draw = ImageDraw.Draw(img)
draw.text((X//2-1-w//2, Y//2-1-h//2),txt,fill= generate_random_color(),font=fnt)
pixels=set_pixels(pixels,w,h,X//2-1-w//2, Y//2-1-h//2)
for i in range(1,len(dct)):
    flag=0
    txt=dct[i][0]
    font_size=int((dct[i][1]*100)/maximum)   
    if font_size<=10:
        font_size=15
    fnt = ImageFont.truetype("times.ttf",font_size)
    w,h=get_text_dimensions(txt, fnt)
    hit=0
    while flag!=1:
        x_coordinate,y_coordinate=get_x_and_y(0,X,Y)
        if (x_coordinate+w)<X and (y_coordinate+h)<Y:
            flag=check_if_possible(pixels,x_coordinate,y_coordinate,w,h)
        if hit>1000:
            break
        hit+=1
        
    draw.text((x_coordinate, y_coordinate),txt,fill= generate_random_color(),font=fnt)
    pixels=set_pixels(pixels,w,h,x_coordinate, y_coordinate)
print("                                             WORD CLOUD GENERTOR                           ")
display(img)