# plotly_tabular_tool - plotly.express wrapped as a Galaxy tool.

## Install to your Galaxy server from the toolshed - search for plotly_tabular_tool owned by fubar2

### Example interactive plots and more at https://lazarus.name/demo/

#### Non interactive screen grab of the tool output
![Plotly blast html output screengrab](plotly_tabular_iris_sample.png)

Galaxy tool to create plotly interactive hover detail HTML plots from user selected columns of any Galaxy tabular data.
## Recommended only for low dimensional data - a few thousand rows
Otherwise file sizes get huge and hover is useless to the viewer, so use non-interactive pdf for bigger data please.

![Plotly tabular Galaxy tool form to generate the example](plotlytabular_toolform_sample.png)

Plotly.express makes a lot of clever design decisions.
Unfortunately, it gets totally confused with very small floats in scientific notation. Treats columns with 5.00e-204 as strings or something, so
strange and probably uninformative axes and plots will probably result if you try a blast evalue column without transformation.
Note that all columns used for colour (legend) and the x/y axis tickmarks are truncated because they can squish up the plot.
*..* is appended at the truncation.

A specialised version for 25 column Galaxy blastn search outputs is also available. It uses this code mostly, but adds a default header and auto-transformation of the evalue column -log10(x) to make them more like the bitscore

## Tool made with the Galaxy ToolFactory: https://github.com/fubar2/galaxy_tf_overlay
The current release includes this and a generic tabular version, and a java .jar wrapper in a history where the generating
ToolFactory form can be recreated using the redo button. Editing the tool id will make a new tool, so all other edits to parameters can be
made and the new tool generated without destroying the original sample.


