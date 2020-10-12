'''

'''
import matplotlib.pyplot as plt
import plotly.graph_objs as go

from plotly.offline import plot
from tagcloud import TagCloud
from wordcloud import WordCloud



# generate wordcloud
tc = TagCloud(fnt_scalar=150, ngrams=1, tfile="doin-time.txt")
tc.generate_cloud()
img = tc.to_image()
img.show()

'''
text = ""
with open("clean.txt", 'r') as f :
	text = f.readline()
	
wc = WordCloud(width=800, height=400, prefer_horizontal=1)
wc.generate(text)
image = wc.to_image()

# extract wordcloud properties
x1, y1, x2, y2 = image.getbbox()
wi = x2 - x1
hi = y2 - y1

toks = []
freqs = []
xs = []
ys = []
fsize = []
colors = []

for (word, freq), size, (x,y), orient, color in wc.layout_ :
	toks.append(word)
	freqs.append(freq*100)
	xs.append(x)
	ys.append(y)
	fsize.append(size)
	colors.append(color)

# invert y-coordinates
max_y = max(ys)
ys = [max_y - y for y in ys]



# convert to interactive text scatter plot	
trace = go.Scatter(
	x=xs, dx=1,
	y=ys, dy=1,
	hoverinfo="text",
	hovertext=['{} : ({},{})'.format(w,x,y) for w,x,y in zip(toks, xs, ys)],
	mode="text+markers",
	text=toks,
	textfont=dict(size=fsize, color=colors),
	textposition="bottom right"
	)
	
lay = go.Layout({
	"xaxis" : {"showgrid":False, "showticklabels":False, "zeroline":False},
	"yaxis" : {"showgrid":False, "showticklabels":False, "zeroline":False}
	})

fig = go.Figure(data=[trace], layout=None)
plot(fig)

image.show()
''' 
print("\nDONE!")
