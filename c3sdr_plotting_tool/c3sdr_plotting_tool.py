import numbers

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from plotly.subplots import make_subplots

# Set the default width and height in pixels for saving plots as a static image.
pio.kaleido.scope.default_width = 1200
pio.kaleido.scope.default_height = 600


class Plotter(object):
    """
    Plotting tool for C3S data rescue project.
    """

    def __init__(self, layout=None, vertical_spacing=None, horizontal_spacing=None, layout_specs=None, title=None,
                 subplot_titles=None, legend=None, white_background=False, font_family=None, font_size=None,
                 font_color=None):
        """
        Initialise a Plotter object with the layout for a figure.

        :param layout:
            Can be omitted for a single plot. For multiple subplots a list with the number of rows followed by the
            number of columns.
        :param vertical_spacing:
            Optional. The vertical spacing between subplots as a fraction of the figure.
        :param horizontal_spacing:
            Optional. The horizontal spacing between subplots as a fraction of the figure.
        :param layout_specs:
            Optional. Specs for the layout. Takes the form of a nested list of dictionaries with one for each position
            in the layout grid. An empty dictionary indicates the default options for a plot, which means that the plot
            is expected to have Cartesian axes and takes one position in the grid. {'rowspan': n} or {'colspan': n}
            indicates a row or column that spans n rows or columns. Unused rows or columns must have None rather than a
            dictionary. {'t': f}, {'b': f}, {'l': f} or {'r': f} indicates the padding of the plot as a fraction, f, of
            the figure from the top, bottom, left or right respectively. {'type': 'geo'} indicates a geo map will be
            present in that position and {'type': 'mapbox'} indicates a mapbox map will be present, rather than a plot
            with Cartesian axes. (Note that if a layout is not specified then it is not necessary to specify that the
            plot will be a map.) E.g. [[{'colspan': 2, 'l': 0.275, 'r': 0.275}, None], [{}, {'type': 'geo'}]] indicates
            a triangular layout with a geo map in the lower right corner. See https://plotly.com/python/subplots/
        :param title:
            Optional. The title of the plot in a single plot figure, or the entire figure in a figure with subplots.
        :param subplot_titles:
            Optional. The titles of the subplots in a multiplot figure from top left to bottom right in a list.
        :param legend:
            Whether to show the legend or not. Automatic by default.
        :param white_background:
            Make the background white and the axis lines black for producing static images. By default the gridlines
            are still shown in very light grey. They can be turned on or off on a per plot basis using the
            show_x_grid and show_y_grid keywords of create_plot. The zero lines can be turned on and off with
            x_zero_line and y_zero_line. The axis lines can be turned on and off with show_x_axis and
            show_y_axis.
        :param font_family:
            Optional. Sets the global font family. Possible values include 'Arial', 'Courier New' and 'Times New Roman'.
            A comma separated list indicates the order of preference to use fonts if one or more is not available on the
            system. Default of None indicates '"Open Sans", verdana, arial, sans-serif'.
        :param font_size:
            Optional. Sets the global font size in points. Default of None indicates 12.
        :param font_color:
            Optional. Sets the global font color. Named CSS colors may be specified. For example, see:
            https://developer.mozilla.org/en-US/docs/Web/CSS/color_value Default of None indicates '#444'
        """
        if layout is None:
            # There is one single plot in the figure.
            self._fig = go.Figure()
        else:
            # There are multiple plots in the figure.
            rows, cols = layout
            self._fig = make_subplots(rows, cols, horizontal_spacing=horizontal_spacing,
                                      vertical_spacing=vertical_spacing, specs=layout_specs,
                                      subplot_titles=subplot_titles)
        # Set the title, whether to show the legend and the global font properties.
        self._fig.update_layout(
            dict(
                title=title,
                showlegend=legend,
                font = dict(
                    family=font_family,
                    size=font_size,
                    color=font_color
                )
            )
        )
        if white_background:
            # Set the background of the whole figure to white.
            self._fig.update_layout({
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white'
            })
        # Store the layout and whether the figure has a white background for future reference.
        self._layout = layout
        self._white_background = white_background

    def create_plot(self, x, y, z=None, e=None, plot_type=None, marker_type=None, marker_size=None, nbins=None,
                    cmin=None, cmax=None, data_flags=None, flags=None, plot_label=None, xlabel=None, ylabel=None,
                    xrange=None, yrange=None, center=None, radius=None, zoom=None, position=None, overplot=False,
                    robust_stats=False, outliers=None, min_n=20, color=None, selected_marker_size=None,
                    selected_marker_color=None, unselected_marker_size=None, unselected_marker_color=None, mode=None,
                    mapbox_style=None, show_x_grid=True, show_y_grid=True, x_zero_line=True, y_zero_line=True,
                    show_x_axis=True, show_y_axis=True, x_tick_angle=None, y_tick_angle=None):
        """
        Add a plot to the figure.

        :param x:
            Data to be used as the x-ordinate. If overplot is True this is expected to be 2 dimensional with one row of
            data for each plot.
        :param y:
            Data to be used as the y-ordinate. If overplot is True this is expected to be 2 dimensional with one row of
            data for each plot.
        :param z:
            Optional. For the case of a map contains the data to be plotted at each longitude and latitude. In the case
            that overplot is True will have the same shape as x and y, but valid data only needs to be present for the
            rows where mapping data is expected. So if there are two plots being overplotted and only the first is a
            map z could be [[z1, z2, z3, ...], None].
        :param e:
            Optional. Uncertainty of each data point. If included then errorbars on the Y-axis will be plotted.
        :param plot_type:
            Type of plot that is to be used to plot x and y. This can be ‘scatter’ for a scatter plot,  ‘hist2d’ for a
            2D histogram plot, ‘mean’ for a mean binned in the x-ordinate,  ‘mean_and_uncert’ for mean values with error
            bars based on the standard error on the mean included, ‘scattergeo’,  'scattermapbox' or 'densitymapbox'
            for the data plotted on a map (assumed relevant data is in x=latitude,y=longitude format and z array needs
            to be present), For time series plots scatter may be used with x in date form. If overplot is True may be a
            list of types for each individual plot or a single string indicating the type of all plots. Defaults to
            ‘scatter’ if None.
        :param marker_type:
            Optional. Contains marker type for plots that use a marker ('scatter', 'scattergeo', 'mean' and
            'mean_and_uncert', but not 'scattermapbox'). Will be ignored for other plot types.
            See https://plotly.com/python/marker-style/#custom-marker-symbols
        :param marker_size:
            Optional. Size of the marker. Defaults to Plotly default.
        :param nbins:
            Optional. For '2dhist', 'mean' or 'mean_and_uncert' plot defines the number of bins to plot. If a scalar and
            overplotting is True then apply to all '2dhist'/'mean'/'mean_and_uncert' plots. If an array or a list then
            must have the same number of elements as the number of plots, but only rows corresponding to '2dhist',
            'mean', or 'mean_and_uncert' plots need to contain data. If the value is negative or None then ignore.
            Default value of None means ignore for all plots.
        :param cmin:
            Optional. Minimum value for 2D histogram or map which allows cutting off of the image. Default is no limit.
            If overplot is True and scalar apply to all'2dhist'/'map' plots. If an array or a list then has to have the
            same number of elements as number of plots, but only elements corresponding to '2dhist' or 'map' plots need
            to contain data. If the value is negative or None then ignore. Default value of None means ignore for all
            plots. If cmin is set, cmax must be set too.
        :param cmax:
            Optional. Maximum value for 2D histogram or map which allows cutting off of the image. Default is no limit.
            If overplot is True and scalar apply to all'2dhist'/'map' plots. If an array or a list then has to have the
            same number of elements as number of plots, but only elements corresponding to '2dhist' or 'map' plots need
            to contain data. If the value is negative or None then ignore. Default value of None means ignore for all
            plots. If cmax is set cmin must be set too.
        :param data_flags:
            Optional. Input data flags from data. Can have an extra dimension to the x/y arrays if multiple flags are to
            be used in the filtering e.g. if ‘scan_quality’ and ‘pixel_quality’ are used for the case where
            x[0:5,0:10000] then the dimension of data_flags would be data_flags[0:2,0:5,0:10000]. Note that it is up to
            the user to fill this array from the flags in the original data file and to deal with the fact that, for
            example, ‘scan_quality’ has one value per scanline and ‘pixel_quality’ has a value per pixel.
        :param flags:
            Optional. Flag value to use with the data_flags file filtering. Flag check is done using a bitwise OR of the
            data_flags against flags > 0. Will have the dimension of the number of input flags e.g. for
            data_flags[0:2,0:5,0:10000] the dimension of be flags[0:2]. Default behaviour is no flagging. This may also
            be done interactively within the plot tool.
        :param plot_label:
            Optional. Label of the plot to appear in the legend. If overplot is True then may be a list. Default
            value of None indicates to use Plotly default labels.
        :param xlabel:
            Optional. String indicating the X axis label. Default is no label.
        :param ylabel:
            Optional. String indicating the Y axis label. Default is no label.
        :param xrange:
            Optional. Specifies the range for the X axis as [xlow, xhigh].
        :param yrange:
            Optional. Specifies the range for the Y axis as [ylow, yhigh].
        :param center:
            Optional. Specifies the center of a mapbox in the form [lon, lat].
        :param zoom:
            Optional. Specifies the zoom of a mapbox.
        :param radius:
            Optional. Specifies the smoothing radius for a densitymapbox heatmap.
        :param position:
            Optional. Position of the plot in the grid for figures with multiple subplots. This is in the form
            [row, col] and is indexed from 1.
        :param overplot:
            Optional. Indicates that there is more than one set of data to be overplotted on the same graph. Default is
            False.
        :param robust_stats:
            Optional. When plotting ‘mean’ or ‘mean_and_uncert’ use robust statistics (median and robust standard
            deviation) instead of mean and standard deviation.  Default is normal statistics.
        :param outliers:
            Optional. If positive then value is threshold for outlier rejection for the ‘mean’ and ‘mean_and_uncert’
            statistics calculation. Default is no outlier rejection.
        :param min_n:
            Optional. When plotting 'mean' or 'mean_and_uncert' plots the minimum number of points per bin acceptable
            in calculating statistics.
        :param color:
            Optional. Define color or color table for each dataset. See, for example, for individual colours:
            https://developer.mozilla.org/en-US/docs/Web/CSS/color_value and for colorscales:
            https://plotly.com/python/builtin-colorscales/ If overplot is True this may be a list, with one
            element for each plot, or a single value that applies to all plots.
        :param selected_marker_size
            Optional. Specify a different size for the markers of selected points. If overplot is True this may be a
            list, with one element for each plot, or a single value that applies to all plots.
        :param selected_marker_color:
            Optional. Specify a different color for the markers of selected points. If overplot is True this may be a
            list, with one element for each plot, or a single value that applies to all plots.
        :param unselected_marker_size
            Optional. Specify a different size for the markers of unselected points. If overplot is True this may be a
            list, with one element for each plot, or a single value that applies to all plots.
        :param unselected_marker_color:
            Optional. Specify a different color for the markers of unselected points. If overplot is True this may be a
            list, with one element for each plot, or a single value that applies to all plots.
        :param mode:
            Optional. For scatter and mean plots specify whether to plot 'lines', 'markers' or 'lines+markers'. The
            default of None indicates a mode of 'markers'. If overplot is True this may be a list, with one element for
            each plot, or a single value that applies to all plots.
        :param mapbox_style:
            Optional. Style of the mapbox tiles. Default of None indicates 'stamen-terrain'. Other possibilities are:
            'open-street-map', 'carto-positron', 'carto-darkmatter', 'stamen-toner' or 'stamen-watercolor'. These are
            raster tiles that do not require sign up or a mapbox access token. There are also vector tiles that do,
            but this is not implemented yet.
        :param show_x_grid:
            Optional. Whether to show grid lines for the x axis for scatter plots and mean plots. Default is True.
        :param show_y_grid:
            Optional. Whether to show grid lines for the y axis for scatter plots and mean plots. Default is True.
        :param x_zero_line:
            Optional. Whether to show the zero line for the x axis for scatter plots and mean plots. Default is True.
        :param y_zero_line:
            Optional. Whether to show the zero line for the y axis for scatter plots and mean plots. Default is True.
        :param show_x_axis:
            Optional. Whether to show the line for the x axis for scatter and mean plots. Default is True.
        :param show_y_axis:
            Optional. Whether to show the line for the y axis for scatter and mean plots. Default is True.
        :param x_tick_angle:
            Optional. Angle to rotate the x axis labels by. Default of None means no rotation.
        :param y_tick_angle:
            Optional. Angle to rotate the y axis labels by. Default of None means no rotation.
        """
        # If row and col specify the position of the plot on the layout if not None.
        if position is None:
            row = None
            col = None
        else:
            row, col = position

        if overplot:
            # If overplotting the data is expected to be a 2D array with data for each trace in each row. Other
            # parameters are also unpacked if they lists/arrays.
            for i, (xi, yi) in enumerate(zip(x, y)):
                zi = None if z is None else z[i]
                ei = None if e is None else e[i]
                pt = None if plot_type is None else plot_type if isinstance(plot_type, str) else plot_type[i]
                pl = None if plot_label is None else plot_label[i]
                nb = None if nbins is None else nbins if isinstance(nbins, numbers.Number) else nbins[i]
                cn = None if cmin is None else cmin if isinstance(cmin, numbers.Number) else cmin[i]
                cx = None if cmax is None else cmax if isinstance(cmax, numbers.Number) else cmax[i]
                mt = None if marker_type is None else marker_type if isinstance(marker_type, str) else marker_type[i]
                ms = None if marker_size is None else \
                    marker_size if isinstance(marker_size, numbers.Number) else marker_size[i]
                c = None if color is None else color if isinstance(color, str) else color[i]
                sms = None if selected_marker_size is None else \
                    selected_marker_size if isinstance(selected_marker_size, numbers.Number) else \
                        selected_marker_size[i]
                smc = None if selected_marker_color is None else \
                    selected_marker_color if isinstance(selected_marker_color, str) else selected_marker_color[i]
                ums = None if unselected_marker_size is None else \
                    unselected_marker_size if isinstance(unselected_marker_size, numbers.Number) else \
                        unselected_marker_size[i]
                umc = None if unselected_marker_color is None else \
                    unselected_marker_color if isinstance(unselected_marker_color, str) else unselected_marker_color[i]
                r = None if radius is None else radius if isinstance(radius, numbers.Number) else radius[i]
                m = None if mode is None else mode if isinstance(mode, str) else mode[i]
                # Add each trace at the specified position
                self._add_trace(row, col, i, pt, xi, yi, zi, ei, pl, c, nb, cn, cx, mt, ms, xrange, yrange, r, sms, smc,
                                ums, umc, m, robust_stats, min_n, outliers)
        else:
            # Add the trace at the specified position
            self._add_trace(row, col, None, plot_type, x, y, z, e, plot_label, color, nbins, cmin, cmax, marker_type,
                            marker_size, xrange, yrange, radius, selected_marker_size, selected_marker_color,
                            unselected_marker_size, unselected_marker_color, mode, robust_stats, min_n, outliers)

        # Update the layout of the plot with the axis labels and ranges. If no layout is specified this is done using
        # the update_layout method of the figure, otherwise it must be done using a method specific to the axis type of
        # the plot.
        if plot_type == 'scattergeo':
            if self._layout is None:
                self._fig.update_layout(
                    geo=dict(
                        lonaxis=dict(
                            range=xrange
                        ),
                        lataxis=dict(
                            range=yrange
                        )
                    )
                )
            else:
                self._fig.update_geos(dict(
                    lonaxis=dict(
                        range=xrange
                    ),
                    lataxis=dict(
                        range=yrange
                    )
                ), row=row, col=col)
        elif plot_type == 'scattermapbox' or plot_type == 'densitymapbox':
            # Mapboxes are slightly different in that a lon/lat of the centre of the plot and a zoom level are
            # specified. The style of the map tiles is also specified here.
            lon, lat = (None, None) if center is None else center
            if mapbox_style is None:
                mapbox_style='stamen-terrain'
            if self._layout is None:
                self._fig.update_layout(
                    mapbox=dict(
                        style=mapbox_style,
                        center={'lon': lon, 'lat': lat},
                        zoom=zoom
                    )
                )
            else:
                self._fig.update_mapboxes(dict(
                    style=mapbox_style,
                    center={'lon': lon, 'lat': lat},
                    zoom=zoom
                ), row=row, col=col)
        else:
            # Cartesian plots, which also include extra options for the grid, zero line, axis line and tick angle.
            if self._layout is None:
                self._fig.update_layout(
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    xaxis=dict(range=xrange,
                               showgrid=show_x_grid,
                               zeroline=x_zero_line,
                               showline=show_x_axis,
                               tickangle=x_tick_angle),
                    yaxis=dict(range=yrange,
                               showgrid=show_y_grid,
                               zeroline=y_zero_line,
                               showline=show_y_axis,
                               tickangle=y_tick_angle)
                )
                if self._white_background:
                    # If the figure has a white background change the colours of the axis and zero lines to black and
                    # the colour of the grid lines to very light grey.
                    self._fig.update_layout(
                        xaxis=dict(
                            linecolor='black',
                            zerolinecolor='black',
                            gridcolor='#CDCDCD'
                        ),
                        yaxis=dict(
                            linecolor='black',
                            zerolinecolor='black',
                            gridcolor='#CDCDCD'
                        )
                    )
            else:
                self._fig.update_xaxes(title_text=xlabel, range=xrange, showgrid=show_x_grid,
                                       zeroline=x_zero_line, showline=show_x_axis, tickangle=x_tick_angle,
                                       row=row, col=col)
                self._fig.update_yaxes(title_text=ylabel, range=yrange, showgrid=show_y_grid,
                                       zeroline=y_zero_line, showline=show_y_axis, tickangle=y_tick_angle,
                                       row=row, col=col)
                if self._white_background:
                    self._fig.update_xaxes(linecolor='black', zerolinecolor='black', gridcolor='#CDCDCD')
                    self._fig.update_yaxes(linecolor='black', zerolinecolor='black', gridcolor='#CDCDCD')

    def _add_trace(self, row, col, i, plot_type, x, y, z, e, plot_label, color, nbins, cmin, cmax, marker_type,
                   marker_size, xrange, yrange, radius, selected_marker_size, selected_marker_color,
                   unselected_marker_size, unselected_marker_color, mode, robust_stats, min_n, outliers):
        """
        Add a trace to a figure.

        :param row:
            Row position in the figure. May be None if only one plot in figure.
        :param col:
            Column position in the figure. May be None if only one plot in figure.
        :param i:
            The index of the plot if overplotting.
        :param plot_type:
            See docstring of create_plot method. Only applies to individual trace.
        :param x:
            See docstring of create_plot method. Only applies to individual trace.
        :param y:
            See docstring of create_plot method. Only applies to individual trace.
        :param z:
            See docstring of create_plot method. Only applies to individual trace.
        :param e:
            See docstring of create_plot method. Only applies to individual trace.
        :param plot_label:
            See docstring of create_plot method. Only applies to individual trace.
        :param color:
            See docstring of create_plot method. Only applies to individual trace.
        :param nbins:
            See docstring of create_plot method. Only applies to individual trace.
        :param cmin:
            See docstring of create_plot method. Only applies to individual trace.
        :param cmax:
            See docstring of create_plot method. Only applies to individual trace.
        :param marker_type:
            See docstring of create_plot method. Only applies to individual trace.
        :param marker_size:
            See docstring of create_plot method. Only applies to individual trace.
        :param xrange:
            See docstring of create_plot method. Only applies to individual trace.
        :param yrange:
            See docstring of create_plot method. Only applies to individual trace.
        :param radius:
            See docstring of create_plot method. Only applies to individual trace.
        :param selected_marker_size:
            See docstring of create_plot method. Only applies to individual trace.
        :param selected_marker_color:
            See docstring of create_plot method. Only applies to individual trace.
        :param unselected_marker_size:
            See docstring of create_plot method. Only applies to individual trace.
        :param unselected_marker_color:
            See docstring of create_plot method. Only applies to individual trace.
        :param mode:
            See docstring of create_plot method. Only applies to individual trace.
        :param robust_stats:
            See docstring of create_plot method.
        :param min_n:
            See docstring of create_plot method.
        :param outliers:
            See docstring of create_plot method.
        """
        # Give the legend group for this subplot a unique identifier so that the legend is grouped by plots.
        lg = None if self._layout is None else chr(97 + (row - 1) * self._layout[0] + (col - 1))
        # A negative number of bins is equivalent to nbins is None.
        if type(nbins) is int and nbins < 0:
            nbins = None
        # A negative cutoff is equivalent to cutoff is None.
        if type(cmin) is int and cmin < 0:
            cmin = None
        if type(cmax) is int and cmax < 0:
            cmax = None
        if plot_type is None or plot_type == 'scatter':
            trace = self.create_scatter_plot(x, y, e, mode, color, marker_size, marker_type, selected_marker_color,
                                             selected_marker_size, unselected_marker_color, unselected_marker_size,
                                             plot_label, lg)
        elif plot_type == 'mean' or plot_type == 'mean_and_uncert':
            if np.ma.is_masked(y) or np.ma.is_masked(x):
                mask = y.mask
                assert (x.mask == mask).all(), 'X and Y have different masks.'
                x = x.data[~mask]
                y = y.data[~mask]
            # Bin the data and take means
            if nbins is None:
                nbins = 'auto'
            hist, bin_edges = np.histogram(x, bins=nbins, range=xrange)
            assert hist.max() >= min_n, 'Insufficient number of data points per bin.'
            digitized = np.digitize(x, bin_edges)
            n_bin_edges = len(bin_edges)
            if robust_stats:
                nbins = n_bin_edges - 1
                binned_data = [y[digitized == i] for i in range(1, n_bin_edges)]
                means, uncert = self.calculate_robust_statistics(y, hist, binned_data, nbins)
                if outliers is not None:
                    binned_data = [binned_data[i][(binned_data[i] - means[i]) / uncert[i] < outliers]
                                   for i in range(nbins)]
                    hist = np.array([len(binned_data[i]) for i in range(nbins)])
                    assert hist.max() >= min_n, 'Insufficient number of data points per bin after outlier rejection.'
                    means, uncert = self.calculate_robust_statistics(y, hist, binned_data, nbins)
            else:
                means = np.array([y[digitized == i].mean() for i in range(1, n_bin_edges)])
            bin_centres = np.mean(np.vstack([bin_edges[0:-1], bin_edges[1:]]), axis=0)
            if plot_type == 'mean':
                uncert = None
            else:
                if not robust_stats:
                    stds = np.array([y[digitized == i].std() for i in range(1, n_bin_edges)])
                    uncert = stds / np.sqrt(hist)
            trace = self.create_scatter_plot(bin_centres, means, uncert, mode, color, marker_size, marker_type,
                                             selected_marker_color, selected_marker_size, unselected_marker_color,
                                             unselected_marker_size, plot_label, lg)
        elif plot_type == 'hist2d':
            # Add a trace for a 2D histogram.
            if self._layout is None:
                colorbar = None
            else:
                # If the plot is a subplot, position the colorbar next to the individual subplot rather than to the
                # right of the whole figure.
                if i is None:
                    i = 0
                xdomain = list(self._fig.select_xaxes(row=row, col=col))[i]['domain']
                ydomain = list(self._fig.select_yaxes(row=row, col=col))[i]['domain']
                colorbar = self.get_colorbar(xdomain, ydomain)
            # Unpack the number of bins and range into X and Y components if appropriate.
            nbinsx = None if nbins is None else nbins if type(nbins) is int else nbins[0]
            nbinsy = None if nbins is None else nbins if type(nbins) is int else nbins[1]
            startx, endx = (None, None) if xrange is None else xrange
            starty, endy = (None, None) if yrange is None else yrange
            trace = go.Histogram2d(x=x, y=y, colorscale=color, colorbar=colorbar, nbinsx=nbinsx, nbinsy=nbinsy,
                                   zmin=cmin, zmax=cmax, xbins=dict(start=startx, end=endx),
                                   ybins=dict(start=starty, end=endy), legendgroup=lg, name=plot_label)
        elif plot_type == 'scattergeo':
            if self._layout is None:
                colorbar = dict(titleside='right')
            else:
                # If the plot is a subplot, position the colorbar next to the individual subplot rather than to the
                # right of the whole figure.
                if i is None:
                    i = 0
                domain = list(self._fig.select_geos(row=row, col=col))[i]['domain']
                xdomain = domain['x']
                ydomain = domain['y']
                colorbar = self.get_colorbar(xdomain, ydomain)
            trace = go.Scattergeo(
                lon=x,
                lat=y,
                marker=dict(
                    color=z,
                    colorscale=color,
                    cmin=cmin,
                    cmax=cmax,
                    colorbar=colorbar,
                    symbol=marker_type,
                    size=marker_size
                ),
                selected=dict(marker=dict(size=selected_marker_size,
                                          color=selected_marker_color)),
                unselected=dict(marker=dict(size=unselected_marker_size,
                                            color=unselected_marker_color)),
                legendgroup=lg,
                name=plot_label
            )
        elif plot_type == 'scattermapbox':
            if self._layout is None:
                colorbar = dict(titleside='right')
            else:
                # If the plot is a subplot, position the colorbar next to the individual subplot rather than to the
                # right of the whole figure.
                if i is None:
                    i = 0
                domain = list(self._fig.select_mapboxes(row=row, col=col))[i]['domain']
                xdomain = domain['x']
                ydomain = domain['y']
                colorbar = self.get_colorbar(xdomain, ydomain)
            trace = go.Scattermapbox(
                lon=x,
                lat=y,
                marker=dict(
                    color=z,
                    colorscale=color,
                    cmin=cmin,
                    cmax=cmax,
                    colorbar=colorbar,
                    size=marker_size
                ),
                selected=dict(marker=dict(size=selected_marker_size,
                                          color=selected_marker_color)),
                unselected=dict(marker=dict(size=unselected_marker_size,
                                            color=unselected_marker_color)),
                legendgroup=lg,
                name=plot_label
            )
        elif plot_type == 'densitymapbox':
            if self._layout is None:
                colorbar = dict(titleside='right')
            else:
                # If the plot is a subplot, position the colorbar next to the individual subplot rather than to the
                # right of the whole figure.
                if i is None:
                    i = 0
                domain = list(self._fig.select_mapboxes(row=row, col=col))[i]['domain']
                xdomain = domain['x']
                ydomain = domain['y']
                colorbar = self.get_colorbar(xdomain, ydomain)
            trace = go.Densitymapbox(
                lon=x,
                lat=y,
                z=z,
                colorscale=color,
                zmin=cmin,
                zmax=cmax,
                colorbar=colorbar,
                radius=radius,
                legendgroup=lg,
                name=plot_label
            )
        else:
            raise ValueError('Plot type not recognized.')
        # Add the plot to the figure.
        self._fig.add_trace(trace, row=row, col=col)

    @classmethod
    def calculate_robust_statistics(cls, y, hist, binned_data, nbins):
        """
        Calculate robust statistics.
        :param y:
        :param hist:
        :param binned_data:
        :param nbins:
        :return:
            The median and the robust standard deviation.
        """
        means = np.array([np.median(binned_data[i]) for i in range(nbins)])
        stds = np.array([np.subtract(*np.percentile(binned_data[i], [75, 25])) / 1.349 for i in range(nbins)])
        uncert = stds / np.sqrt(hist)
        return means, uncert

    @classmethod
    def create_scatter_plot(cls, x, y, e, mode, color, marker_size, marker_type, selected_marker_color,
                            selected_marker_size, unselected_marker_color, unselected_marker_size, plot_label, lg):
        """
        Create a scatter plot or line plot. Needed for the case of mean and mean and uncertainty plots as well as
        scatter plots.
        :param x:
        :param y:
        :param e:
        :param mode:
        :param color:
        :param marker_size:
        :param marker_type:
        :param selected_marker_color:
        :param selected_marker_size:
        :param unselected_marker_color:
        :param unselected_marker_size:
        :param plot_label:
        :param lg:
            The legend group of the plot.
        :return:
        """
        if e is None:
            error = None
        else:
            # Plot error bars
            error = dict(type='data',
                         array=e,
                         visible=True)
        # Add a trace for a scatter plot.
        if mode is None or mode == 'markers':
            trace = go.Scattergl(x=x, y=y, mode='markers', marker={'symbol': marker_type,
                                                                   'color': color,
                                                                   'size': marker_size},
                                 selected={'marker': {'size': selected_marker_size,
                                                      'color': selected_marker_color}},
                                 unselected={'marker': {'size': unselected_marker_size,
                                                        'color': unselected_marker_color}},
                                 error_y=error,
                                 legendgroup=lg, name=plot_label)
        elif mode == 'lines+markers':
            trace = go.Scattergl(x=x, y=y, line={'color': color}, marker={'symbol': marker_type,
                                                                          'color': color,
                                                                          'size': marker_size},
                                 selected={'marker': {'size': selected_marker_size,
                                                      'color': selected_marker_color}},
                                 unselected={'marker': {'size': unselected_marker_size,
                                                        'color': unselected_marker_color}},
                                 error_y=error,
                                 mode='lines+markers', name=plot_label, legendgroup=lg)
        elif mode == 'lines':
            trace = go.Scattergl(x=x, y=y, line={'color': color}, name=plot_label, legendgroup=lg)
        else:
            raise ValueError('Invalid mode for scatter plot.')
        return trace

    @staticmethod
    def get_colorbar(xdomain, ydomain):
        """
        Create a dictionary specifying the position of the colorbar for 2D histogram and map plots given the x and y
        domains.

        :param xdomain:
            A list in the form [x_low, x_high]
        :param ydomain:
            A list in the form [y_low, y_high]
        :return:
            A dictionary specifying the positioning of the colorbar.
        """
        colorbar = dict(x=xdomain[1],
                        y=ydomain[0],
                        len=ydomain[1] - ydomain[0],
                        xanchor='left',
                        yanchor='bottom',
                        ypad=0)
        return colorbar

    def show_plot(self, height=None, width=None, match_xaxes=False, match_yaxes=False, interactive_selection=False,
                  jupyter=True):
        """
        Display the plot for testing or interactive analysis.

        :param height:
            Optional. The height of the figure in pixels.
        :param width:
            Optional. The width of the figure in pixels.
        :param match_xaxes:
            Optional. Match the zoom of the X axis in subplots.
        :param match_yaxes:
            Optional. Match the zoom of the Y axis in subplots.
        :param interactive_selection:
            Optional. Specify that the plot will have interactive selection features, such as linked selections between
            plots and the ability to save the selected points.
        :param jupyter:
            Optional. Indicates that the plot is within a Jupyter notebook if interactive selection is on. If True then
            the selected point indices will be saved to SELECTED_POINTS_INDS in the notebook on selection.
        :return:
        """
        # Update the height and width of the plot in pixels.
        self._fig.update_layout(
            dict(
                height=height,
                width=width
            )
        )
        # Link the zoom on the Y axes if required.
        if match_xaxes:
            self._fig.update_xaxes(matches='x')
        # Link the zoom on the Y axes if required.
        if match_yaxes:
            self._fig.update_yaxes(matches='y')

        if interactive_selection:
            # Create JavaScript event handlers, which link the selection between plots and if in a Jupyter notebook
            # save the point indices to a variable in the notebook.
            if jupyter:
                js = """
                var ele = document.getElementById("{plot_id}");
                ele.on('plotly_selected', function(eventData){
                    var selectedpoints = [];
                    IPython.notebook.kernel.execute('SELECTED_POINT_INDS = []')
    
                    eventData.points.forEach(function(pt) {
                        selectedpoints.push(pt.pointNumber);
                        IPython.notebook.kernel.execute('SELECTED_POINT_INDS.append(' + pt.pointNumber.toString() +')')
                    });
                    var update = {
                        'selectedpoints': [selectedpoints]
                    };
                    Plotly.restyle("{plot_id}", update)
                });
                ele.on('plotly_deselect', function(){
                    var update = {
                        'selectedpoints': [null]
                    };
                    Plotly.restyle("{plot_id}", update)
                });
                """
            else:
                js = """
                var ele = document.getElementById("{plot_id}");
                ele.on('plotly_selected', function(eventData){
                    var selectedpoints = [];
                    
                    eventData.points.forEach(function(pt) {
                        selectedpoints.push(pt.pointNumber);
                    });
                    var update = {
                        'selectedpoints': [selectedpoints]
                    };
                    Plotly.restyle("{plot_id}", update)
                });
                ele.on('plotly_deselect', function(){
                    var update = {
                        'selectedpoints': [null]
                    };
                    Plotly.restyle("{plot_id}", update)
                });
                """

            # Show the plot with the JavaScript injected into the HTML. See the link below.
            # https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html
            self._fig.show(post_script=js)
        else:
            # If interactive select is not required, simply display the figure.
            self._fig.show()

    def save_plot(self, file, width=None, height=None, scale=None):
        """
        Save the plot to a file, the type of which is indicated by the extension of the filename.

        :param file:
            The path to the file.
        :param width:
            The width in pixels.
        :param height:
            The height in pixels.
        :param scale:
        :return:
        """
        self._fig.write_image(file, width=width, height=height, scale=scale)


if __name__ == '__main__':
    # Example plots
    # plotter = Plotter(title='Scatter plot of millions of points')
    # x = np.random.normal(0, 1, 1000000)
    # y = np.random.normal(0, 1, 1000000)
    # plotter.create_plot(x, y, xlabel='x', ylabel='y', marker_size=2)
    # plotter.show_plot()
    #
    # plotter = Plotter(title='Scatter plot of random data')
    # x1 = np.random.normal(0, 1, 1000)
    # y1 = np.random.normal(0, 1, 1000)
    # x2 = np.random.normal(2, 1, 1000)
    # y2 = np.random.normal(2, 1, 1000)
    # plotter.create_plot([x1, x2], [y1, y2], overplot=True, plot_label=['mean = (0, 0)', 'mean = (2, 2)'],
    #                     xlabel='x', ylabel='y', marker_type=['circle', 'triangle-up'], xrange=[-5, 5], yrange=[-5, 5])
    # plotter.show_plot()
    # # plotter.save_plot('/Users/charles/scatter.pdf')
    #
    # plotter = Plotter(title='2D histogram of random data')
    # x = np.random.normal(0, 1, 100000)
    # y = np.random.normal(0, 1, 100000)
    # plotter.create_plot(x, y, plot_type='hist2d', xlabel='x', ylabel='y', color='viridis', nbins=100, xrange=[-5, 5],
    #                     yrange=[-5, 5])
    # plotter.show_plot()
    #
    # plotter = Plotter(title='Time series of random data')
    # x = np.arange('2000-01', '2001-01', dtype='datetime64[D]')
    # y = np.random.normal(0, 1, 366)
    # plotter.create_plot(x, y, xlabel='Date', ylabel='y', mode='lines', x_tick_angle=45)
    # plotter.show_plot()
    #
    # plotter = Plotter(layout=[4, 2], horizontal_spacing=0.15,
    #                   layout_specs=[[{'colspan': 2, 'l': 0.2875, 'r': 0.2875}, None], [{}, {}],
    #                                 [{'type': 'geo'}, {'type': 'mapbox'}],
    #                                 [{'colspan': 2, 'l': 0.2875, 'r': 0.2875, 'type': 'mapbox'}, None]],
    #                   title='Subplots example', subplot_titles=['Scatter plot of random data',
    #                                                             '2D histogram of random data',
    #                                                             'Time series of random data',
    #                                                             'Scattergeo of random data',
    #                                                             'Scattermapbox of random data',
    #                                                             'Densitymapbox of random data'],
    #                   white_background=True, font_family='Times New Roman', font_size=18, font_color='black')
    # x1 = np.random.normal(0, 1, 1000)
    # y1 = np.random.normal(0, 1, 1000)
    # x2 = np.random.normal(2, 1, 1000)
    # y2 = np.random.normal(2, 1, 1000)
    # plotter.create_plot([x1, x2], [y1, y2], position=[1, 1], overplot=True,
    #                     plot_label=['mean = (0, 0)', 'mean = (2, 2)'],
    #                     xlabel='x', ylabel='y', marker_type=['circle', 'triangle-up'], marker_size=[5, 5],
    #                     xrange=[-5, 5], yrange=[-5, 5], color=['steelblue', 'green'],
    #                     selected_marker_color=['red', 'orange'], show_x_axis=False, show_y_axis=False)
    # x = np.random.normal(0, 1, 100000)
    # y = np.random.normal(0, 1, 100000)
    # plotter.create_plot(x, y, position=[2, 1], plot_type='hist2d', xlabel='x', ylabel='y', color='viridis', nbins=100,
    #                     cmin=0, cmax=95, xrange=[-5, 5], yrange=[-5, 5])
    # x = np.arange('2000-01', '2001-01', dtype='datetime64[D]')
    # y = np.random.normal(0, 1, 366)
    # plotter.create_plot(x, y, position=[2, 2], mode='lines', xlabel='Date', ylabel='y', show_y_grid=False,
    #                     show_x_axis=False, x_tick_angle=45, plot_label='time series data')
    # lons = np.random.random(1000) * 360.0
    # lats = np.random.random(1000) * 180.0 - 90.0
    # z = np.random.random(1000) * 50.0
    # plotter.create_plot(lons, lats, z, position=[3, 1], xrange=[-90.0, 90.0], yrange=[-45.0, 45.0],
    #                     plot_type='scattergeo', marker_type='square', marker_size=5,
    #                     selected_marker_color='green', plot_label='geo data')
    # lons = np.random.random(100000) * 360.0
    # lats = np.random.random(100000) * 180.0 - 90.0
    # z = np.random.random(100000) * 50.0
    # plotter.create_plot(lons, lats, z, position=[3, 2], plot_type='scattermapbox', marker_size=2,
    #                     selected_marker_color='green', unselected_marker_color='orange', plot_label='mapbox data')
    # lons = np.random.random(1000) * 360.0
    # lats = np.random.random(1000) * 180.0 - 90.0
    # z = np.random.random(1000) * 50.0
    # plotter.create_plot(lons, lats, z, position=[4, 1], plot_type='densitymapbox', radius=10,
    #                     plot_label='mapbox data')
    # plotter.show_plot(height=1800)
    # # plotter.save_plot('/Users/charles/subplots.pdf')
    #
    # plotter = Plotter(title='Map of random data')
    # lons = np.random.random(10000) * 360.0
    # lats = np.random.random(10000) * 180.0 - 90.0
    # z = np.random.random(10000) * 50.0
    # plotter.create_plot(lons, lats, z, xrange=[-90.0, 90.0], yrange=[-45.0, 45.0], plot_type='scattergeo',
    #                     marker_type='square', marker_size=2, plot_label='map data')
    # plotter.show_plot()
    #
    # plotter = Plotter(title='Map of random data')
    # lons = np.random.random(10000) * 360.0
    # lats = np.random.random(10000) * 180.0 - 90.0
    # z = np.random.random(10000) * 50.0
    # plotter.create_plot(lons, lats, z, plot_type='scattermapbox', marker_size=2, plot_label='map data',
    #                     mapbox_style='carto-positron')
    # plotter.show_plot()
    #
    # plotter = Plotter(title='Compare data on hover example')
    # x = np.arange(0, 100)
    # y1 = np.random.normal(0, 1, 100)
    # y2 = np.random.normal(0, 1, 100)
    # plotter.create_plot([x, x], [y1, y2], xlabel='x', ylabel='y', overplot=True)
    # plotter.show_plot()
    #
    # plotter = Plotter(title='Error bars example')
    # x = np.arange(0, 100)
    # y = np.random.normal(0, 1, 100)
    # e = np.random.normal(0, 0.1, 100)
    # plotter.create_plot(x, y, e=e, xlabel='x', ylabel='y')
    # plotter.show_plot()

    plotter = Plotter(title='Mean plot example')
    x = np.arange(1000000)
    y = np.arange(1000000)
    plotter.create_plot(x, y, xlabel='x', ylabel='y', xrange=[250000, 750000], plot_type='mean')
    plotter.show_plot()

    plotter = Plotter(title='Mean and uncertainty plot example')
    plotter.create_plot(x, y, xlabel='x', ylabel='y', xrange=[250000, 750000], plot_type='mean_and_uncert')
    plotter.show_plot()

    plotter = Plotter(title='Mean and uncertainty plot example')
    x = np.arange(1000000)
    y = np.random.normal(0, 1, 1000000)
    plotter.create_plot(x, y, xlabel='x', ylabel='y', nbins=100, plot_type='mean_and_uncert')
    plotter.show_plot()

    plotter = Plotter(title='Mean and uncertainty plot example with robust stats')
    plotter.create_plot(x, y, xlabel='x', ylabel='y', nbins=100, robust_stats=True, plot_type='mean_and_uncert')
    plotter.show_plot()

    plotter = Plotter(title='Mean and uncertainty plot with masked data example')
    mask = np.zeros(1000000, dtype='int32')
    mask[np.arange(0, 1000000, 1000)] = 1
    x = np.ma.MaskedArray(x, mask=mask)
    y = np.ma.MaskedArray(y, mask=mask)
    plotter.create_plot(x, y, xlabel='x', ylabel='y', nbins=100, plot_type='mean_and_uncert')
    plotter.show_plot()

    plotter = Plotter(title='Mean and uncertainty plot example with robust stats and outlier rejection')
    x = np.arange(1000000)
    y = np.random.gamma(4, size=1000000)
    plotter.create_plot(x, y, xlabel='x', ylabel='y', nbins=100, robust_stats=True, outliers=0.95,
                        plot_type='mean_and_uncert')
    plotter.show_plot()
