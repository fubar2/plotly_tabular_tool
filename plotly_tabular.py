# python script wrapped by the  plotly_tabular ToolFactory generated code.
# once working correctly, wrapping is a matter of filling in a ToolFactory form.
# that gets unpleasant if you have a lot of parameters but works well
# for this kind of application.
import argparse
import shutil
import sys
import plotly.express as px
import pandas as pd
# Ross Lazarus July 2023
# based on various plotly tutorials
MAXHTMLROWS = 5000 # empirically, browsers die at 10k so stop here for safety and give png
parser = argparse.ArgumentParser()
a = parser.add_argument
a('--input_tab',default='')
a('--header',default='')
a('--htmlout',default="test_run.html")
a('--xcol',default=3, type=int)
a('--ycol',default=2, type=int)
a('--colourcol',default=None, type=int)
a('--hovercol',default=None, type=int)
a('--title',default='Default plot title')
a('--image_type',default='short_html')
args = parser.parse_args()
isColour = False
isHover = False
if args.colourcol > 0:
    isColour = True
if args.hovercol > 0:
    isHover = True
df = pd.read_csv(args.input_tab, sep='\t')
MAXLEN=35
NCOLS = df.columns.size
NROWS = len(df.index)
defaultcols = ['col%d' % (x+1) for x in range(NCOLS)]
testcols = df.columns
if args.image_type in ['short_html', 'long_html']: # refuse to create browser crashing gob stopper html
    if NROWS > MAXHTMLROWS:
        sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): 5k+ rows (you supplied %d) in html breaks browsers, so please rerun the job using png format output.' % NROWS)
        sys.exit(6)

if max(args.xcol-1, args.ycol-1) > NCOLS: # out of range
    sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): xcol %d or ycol %d are greater than the number of columns found %d' %(args.xcol, args.ycol, NCOLS))
if isHover and isColour:
    fig = px.scatter(df, x=df.columns[args.xcol-1], y=df.columns[args.ycol-1], color=df.columns[args.colourcol-1], hover_name=df.columns[args.hovercol-1])
elif isHover:
    fig = px.scatter(df, x=df.columns[args.xcol-1], y=df.columns[args.ycol-1], hover_name=df.columns[args.hovercol-1])
elif isColour:
    fig = px.scatter(df, x=df.columns[args.xcol-1], y=df.columns[args.ycol-1],  color=df.columns[args.colourcol-1])
else:
    fig = px.scatter(df, x=df.columns[args.xcol-1], y=df.columns[args.ycol-1], )
if args.title:
    ftitle=dict(text=args.title, font=dict(size=50))
    fig.update_layout(title=ftitle)
for scatter in fig.data:
    scatter['x'] = [str(x)[:MAXLEN] + '..' if len(str(x)) > MAXLEN else x for x in scatter['x']]
    scatter['y'] = [str(x)[:MAXLEN] + '..' if len(str(x)) > MAXLEN else x for x in scatter['y']]
    if args.colourcol > 0:
        sl = str(scatter['legendgroup'])
        if len(sl) > MAXLEN:
            scatter['legendgroup'] = sl[:MAXLEN]
if args.image_type == "short_html":
    fig.write_html(args.htmlout, full_html=False, include_plotlyjs='cdn')
elif args.image_type == "long_html":
    fig.write_html(args.htmlout)
elif args.image_type == "small_png":
    ht = 768
    wdth = 1024
    fig.write_image('plotly.png', height=ht, width=wdth)
    shutil.copyfile('plotly.png', args.htmlout)
else:
    ht = 1200
    wdth = 1920
    fig.write_image('plotly.png', height=ht, width=wdth)
    shutil.copyfile('plotly.png', args.htmlout)
