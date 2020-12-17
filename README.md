C3SDR Plotting Tools
====================

Plotting tools for the C3S Data Rescue project.

The tool in the radsim_data_converter directory is for converting the output of RadSim simulations into a format
compatible with the Level 1 input files.

The tool in the c3sdr_plotting_tool directory is for producing plots produced with the specific requirements of the C3S
Data Rescue project in mind. It uses Plotly (https://plotly.com/python/) to produce interactive plots as well as static
images intended for publication. Scatter plots, 2D histograms, line plots and maps are available. Time series plots can
be produced by passing dates to scatter or line plots.

Multiple plots per figure can be specified in flexible layouts. Please see the tutorial notebook in this directory and
the docstring for the Plotter class for details.

Linking the zoom and the selection between plots is possible both inside and outside Jupyter notebooks, but within a
notebook it is possible to access the indices of selected points on an individual plot or a set of plots with linked
selections. The linked selection function assumes that the data on all the plots is ordered in the same way as it is the
indices of the selected points that are shared between plots. Not having the points on the different plots in the same
order will give erroneous results.

Overplotting is possible and arbitrary plot types can be overplotted, although this may not always make sense. If two
scatter plots are overplotted the linked selection would treat the points in the plots as separate sets of points, which
might produce unexpected results. So, linking the selection between plots with two or more sets of points per plot is
not supported.

There is currently also an issue with Plotly that means that when a map plot is part of a set of plots with linked
selections the first plot might need to be a blank plot to avoid selecting extra points unexpectedly. The main map types
available are scattergeo and mapboxes, which plot points on the map rather than an image. The latter is not currently
possible. There is also the density mapbox plot, which plots a density heatmap rather than points. Mapboxes support
large numbers of points better than scattergeos. 

##Installation

The tool requires Plotly to be installed. The easiest way to do this on your local machine is to download Anaconda
Python (https://www.anaconda.com/products/individual) or Miniconda (https://docs.conda.io/en/latest/miniconda.html).
Plotly can then be installed with the following commands:

```
conda install -c conda-forge plotly
conda install -c plotly python-kaleido
```

Jupyter notebook and numpy, if not installed can be installed with the commands:

```
conda install numpy
conda install jupyter
```

Jupyter notebook can be opened with the command:

```
jupyter notebook
```

This should open a browser with a file manager pointing in your current working directory in which you can create or
open a Python notebook.

The basic workflow of the code is as follows:

```
# Import the library from this directory. It c3sdr_plotting_tools directory is not your current directory, then it must
# be in your PYTHONPATH environment variable.
from c3sdr_plotting_tool import Plotter

# Instantiate a figure with the required layout, to link selections between plots use interactive=True
plotter = Plotter(…)

# Add a plot in a specified position in the figure.
plotter.create_plot(…)
…

# Display or save the plot. To link the zoom uses match_xaxes=True or match_yaxes=True.
plotter.show_plot(…) or plotter.save_plot(…)
```

A tutorial for the tool is given in `plotting_tool_tutorial.ipynb` in this directory. Inline documentation is available
when using a notebook by typing e.g. `plotter.create_plot?` or in Python more generally by typing e.g.
`help(plotter.create_plot)`.