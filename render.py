import matplotlib.pyplot as plt
import plotly.graph_objs as go

from plotly.offline import plot
from tagcloud import TagCloud



# generate wordcloud
tc = TagCloud(fnt_scalar=150, ngrams=1, tfile="doin-time.txt")
tc.generate_cloud()
img = tc.to_image()
#img.show()

# extract wordcloud properties
x1, y1, x2, y2 = img.getbbox()
xcanvas = x2 - x1
ycanvas = y2 - y1

grams = []
freqs = []
sizes = []
fnts = []
dims = []
xs = []
ys = []
colors = []

for (txt, freq, size, fnt, (width, height), (x, y), color) in tc.layout :
	grams.append(txt)
	freqs.append(freq)
	sizes.append(size)
	fnts.append(fnt)
	dims.append((width, height))
	xs.append(x)
	ys.append(y)
	colors.append(color)

# invert y-coordinates
max_y = max(ys)
ys = [max_y - y for y in ys]



# convert to interactive text scatter plot	
trace = go.Scatter(
	x=xs, dx=1,
	y=ys, dy=1,
	hoverinfo="text",
	hovertext=["'{}' raw frequency : {}".format(gram, size) for gram, size in zip(grams, freqs)],
	mode="text+markers",
	text=grams,
	textfont=dict(size=sizes, color=colors),
	textposition="bottom right"
	)
	
lay = go.Layout({
	"xaxis" : {"showgrid":False, "showticklabels":False, "zeroline":False},
	"yaxis" : {"showgrid":False, "showticklabels":False, "zeroline":False},
	"paper_bgcolor" : "black",
	"plot_bgcolor" : "black"
	})

fig = go.Figure(data=[trace], layout=lay)
plot(fig)

 
print("\nDONE!")
