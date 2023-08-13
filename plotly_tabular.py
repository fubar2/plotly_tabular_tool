# python script wrapped by the  plotly_tabular ToolFactory generated code.
# once working correctly, wrapping is a matter of filling in a ToolFactory form.
# that gets unpleasant if you have a lot of parameters but works well
# for this kind of application.
import argparse
import shutil
import sys
import math
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
a('--xcol',default='')
a('--ycol',default='')
a('--colourcol',default='')
a('--hovercol',default='')
a('--title',default='Default plot title')
a('--image_type',default='small_png')
args = parser.parse_args()
isColour = False
isHover = False
if len(args.colourcol.strip()) > 0:
    isColour = True
if len(args.hovercol.strip()) > 0:
    isHover = True
df = pd.read_csv(args.input_tab, sep='\t')
MAXLEN=35
NCOLS = df.columns.size
NROWS = len(df.index)
defaultcols = ['col%d' % (x+1) for x in range(NCOLS)]
testcols = df.columns
if args.image_type in ['short_html', 'long_html']: # refuse to create browser crashing gob stopper html
    if NROWS > MAXHTMLROWS:
        sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): As advised on the tool form, 5k+ rows (you supplied %d) in html breaks browsers, so redo the job but change to png format output.' % NROWS)
        sys.exit(6)
if len(args.header.strip()) > 0:
    newcols = args.header.split(',')
    if len(newcols) == NCOLS:
        if (args.xcol in newcols) and (args.ycol in newcols):
            df.columns = newcols
        else:
            sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): xcol %s and/or ycol %s not found in supplied header parameter %s' % (args.xcol, args.ycol, args.header))
            sys.exit(4)
    else:
        sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): Supplied header %s has %d comma delimited header names - does not match the input tabular file %d columns' % (args.header, len(newcols), NCOLS))
        sys.exit(5)
else: # no header supplied - check for a real one that matches the x and y axis column names
    colsok = (args.xcol in testcols) and (args.ycol in testcols) # if they match, probably ok...should use more code and logic..
    if colsok:
        df.columns = testcols # use actual header
    else:
        colsok = (args.xcol in defaultcols) and (args.ycol in defaultcols)
        if colsok:
            sys.stderr.write('replacing first row of data derived header %s with %s' % (testcols, defaultcols))
            df.columns = defaultcols
        else:
            sys.stderr.write('## CRITICAL USAGE ERROR (not a bug!): xcol %s and ycol %s do not match anything in the file header, supplied header or automatic default column names %s' % (args.xcol, args.ycol, defaultcols))
if isHover and isColour:
    fig = px.scatter(df, x=args.xcol, y=args.ycol, color=args.colourcol, hover_name=args.hovercol)
elif isHover:
    fig = px.scatter(df, x=args.xcol, y=args.ycol, hover_name=args.hovercol)
elif isColour:
    fig = px.scatter(df, x=args.xcol, y=args.ycol, color=args.colourcol)
else:
    fig = px.scatter(df, x=args.xcol, y=args.ycol)
if args.title:
    ftitle=dict(text=args.title, font=dict(size=50))
    fig.update_layout(title=ftitle)
for scatter in fig.data:
    scatter['x'] = [str(x)[:MAXLEN] + '..' if len(str(x)) > MAXLEN else x for x in scatter['x']]
    scatter['y'] = [str(x)[:MAXLEN] + '..' if len(str(x)) > MAXLEN else x for x in scatter['y']]
    if len(args.colourcol.strip()) == 0:
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
