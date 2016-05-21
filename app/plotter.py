import os
import numpy as np

from bokeh.embed import components,file_html
from bokeh.plotting import figure,ColumnDataSource
from bokeh.models import (HoverTool, BoxSelectTool, BoxZoomTool, 
                          PanTool, ResetTool,WheelZoomTool,
                          GMapPlot,GMapOptions,DataRange1d,
                          glyphs,Legend
                         )
from bokeh.resources import CDN
from bokeh.palettes import Spectral6
from bokeh.charts import Bar
from bokeh.io import vplot

from app import app
from data_sprunger import orig_df,df,most_routes_df,longest_route_df,longest_route_name

def save_html(plot,filename,path='.'):
    html = file_html(plot,CDN,filename)
    full_path = os.path.join(path,filename)
    if not os.path.isfile(full_path):
        with open(full_path,'w') as myhtmlfile:
            myhtmlfile.write(html)


def plot_longest_route(dataframe):
    def create_data_source(data_frame):
        return ColumnDataSource(
            data=dict(
            route=data_frame['route'],
            stop_count=data_frame['stop_count'],
            ))
    source = create_data_source(dataframe)
    TOOLS=[HoverTool(tooltips = [('route', '@route'),('stop_count','@stop_count')]),BoxZoomTool(),PanTool(),ResetTool(),WheelZoomTool()]
    p = figure(title="# of Stops per CTA Bus Route", x_axis_label='route', 
               y_axis_label='# of stops',tools=TOOLS)
    
    p.scatter('route','stop_count', source = source)

    p2 = Bar(dataframe[:25], 'route',values='stop_count', title="25 Longest Routes by # of Stops",
            width=800, height=600,ylabel='Stop Count')
    z = vplot(p,p2)

    #save_html(z,'bokeh_longest_route.html')
    figscript,figdiv = components(z)
    return (figscript,figdiv)    

def plot_map(dataframe,all_stops=False,plot_routes=False):
    
    longest = dataframe[dataframe.route==longest_route_name] 
    df_copy = dataframe
    slim_df = df_copy.drop_duplicates(['stop_id'])
    most = slim_df[slim_df['num_routes']==slim_df['num_routes'].max()]
    busiest = slim_df[slim_df['total_traffic']==slim_df['total_traffic'].max()]
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
    source_most = create_data_source(most)
    source_busiest = create_data_source(busiest)
    source_longest = create_data_source(longest)
    map_options = GMapOptions(lat=41.8369, lng=-87.6847, zoom=11,map_type="roadmap")
    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(),map_options=map_options,
            title='CTA Bus Data October 2012')
    if all_stops:
        source = create_data_source(df_copy.drop_duplicates('stop_id'))
        circle = glyphs.Circle(x="lon", y="lat", size=5, fill_color=Spectral6[0], fill_alpha=0.8, line_color=None)
        plot.add_glyph(source,circle)
        filename='bokeh_full_map.html'

    if plot_routes:
        N = len(dataframe['route'].unique())
        route_list = dataframe['route'].unique()
        x = np.random.random(size=N) * 100
        y = np.random.random(size=N) * 100
        colors = ["#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]

        for i,route in enumerate(route_list):
            source = create_data_source(dataframe[dataframe.route==route].sort_values(by=['stop_id']))
            circle = glyphs.Circle(x="lon", y="lat", size=5, fill_color=colors[i], fill_alpha=0.8, line_color=None)
            plot.add_glyph(source,circle)       
            filename='bokeh_route_map.html'

    circle_l = glyphs.Circle(x="lon", y="lat", fill_color="yellow",size=5)
    circle_m = glyphs.Circle(x="lon", y="lat", fill_color="purple",size=10)
    circle_b = glyphs.Circle(x="lon", y="lat", fill_color="red",size=10)
    busiest_colors = ["green","blue"]
    bs_routes = dataframe[dataframe['total_traffic']==dataframe['total_traffic'].max()]['route'].values
    for i,r in enumerate(bs_routes):
        bs_slice = dataframe[dataframe.route==r]
        source_busiest_sliced = create_data_source(bs_slice)
        bs_circle = glyphs.Circle(x="lon", y="lat", fill_color=busiest_colors[i],size=5)    
        plot.add_glyph(source_busiest_sliced,bs_circle)
    cpl = plot.add_glyph(source_longest,circle_l)
    cpm = plot.add_glyph(source_most,circle_m)
    cpb = plot.add_glyph(source_busiest,circle_b)

    legend = Legend(legends=[("Stop on most routes",[cpm]),
                            ("Longest route: %s" % longest_route_name,[cpl]),
                            ("Busiest stop",[cpb])])
    plot.add_layout(legend)

    plot.add_tools(HoverTool(tooltips = [('stop id', '@stop'),('on street','@on_street'),('cross street','@cross_street'),('# of routes','@number_of_routes'),('routes','@routes'),('total traffic','@busiest')]),BoxZoomTool(),PanTool(),ResetTool(),WheelZoomTool())
    if not plot_routes and not all_stops:
        filename = 'bokeh_brief_map.html'
    #save_html(plot,filename)   
    figscript,figdiv = components(plot)

    return (figscript,figdiv)

if __name__=='__main__':
    plot_longest_route(longest_route_df)
    plot_map(df,all_stops=True)
    plot_map(df)
    plot_map(df,plot_routes=True)
