import os
import numpy as np

from bokeh.plotting import ColumnDataSource,output_file
from bokeh.models import (HoverTool, BoxSelectTool, BoxZoomTool, 
                          PanTool, ResetTool,WheelZoomTool,
                          GMapPlot,GMapOptions,DataRange1d,
                          glyphs,Legend
                         )
from bokeh.resources import CDN
from bokeh.charts import show
from bokeh.palettes import Spectral6
import pandas

df = pandas.read_csv('sample_data.csv')
output_file('plots.html')

def plot_map(dataframe):
    df = dataframe.drop_duplicates('stop_id')
    df_stop_on_most_routes = df[df['num_routes']==df['num_routes'].max()]
    def create_data_source(data_frame):
        return ColumnDataSource(
            data=dict(
            stop = data_frame['stop_id'],
            on_street=data_frame['on_street'],
            cross_street=data_frame['cross_street'],
            number_of_routes = data_frame['num_routes'],
            routes = data_frame['routes'],
            busiest = data_frame['total_traffic'],
            lat=data_frame['lat'],
            lon=data_frame['lon'],
            ))
    map_options = GMapOptions(lat=41.8369, lng=-87.6847, zoom=11,map_type="roadmap")
    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(),map_options=map_options,
            title='CTA Bus Data October 2012')
    source = create_data_source(df)
    source_most = create_data_source(df_stop_on_most_routes)
    circle = glyphs.Circle(x="lon", y="lat", size=5, fill_color=Spectral6[0], fill_alpha=0.8, line_color=None)
    plot.add_glyph(source,circle)

    circle_m = glyphs.Circle(x="lon", y="lat", fill_color="purple",size=10)
    cpm = plot.add_glyph(source_most,circle_m)

    legend = Legend(legends=[("Stop on most routes",[cpm])])
    plot.add_layout(legend)

    plot.add_tools(HoverTool(tooltips = [('stop id', '@stop'),('on street','@on_street'),('cross street','@cross_street'),('# of routes','@number_of_routes'),('routes','@routes'),('total traffic','@busiest')]),BoxZoomTool(),PanTool(),ResetTool(),WheelZoomTool())

    return plot

if __name__=='__main__':
    p1 = plot_map(df)
    show(p1)
