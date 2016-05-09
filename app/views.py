from flask import render_template
from app import app
import os

from data_sprunger import orig_df,most_routes_df,df,longest_route_df
from plotter import plot_longest_route,plot_map

@app.route('/index')
def index():   
    return render_template('base.html')

@app.route('/raw_table')
def raw_table():
    return render_template('render_table.html',df = orig_df)

@app.route('/longest_route')
def longest_route():
    figscript,figdiv = plot_longest_route(longest_route_df)
    return render_template('render.html',figscript=figscript,figdiv=figdiv)
        
@app.route('/most_routes')
def most_routes():
    return render_template('render_table.html',df=most_routes_df)
    
@app.route('/brief_map')
def brief_map():
    figscript,figdiv = plot_map(df)
    return render_template('render.html',figscript=figscript,figdiv=figdiv)    

@app.route('/full_map')
def full_map():
    figscript,figdiv = plot_map(df,all_stops=True)
    return render_template('render.html',figscript=figscript,figdiv=figdiv)    

@app.route('/route_map')
def route_map():
    figscript,figdiv = plot_map(df,plot_routes=True)
    return render_template('render.html',figscript=figscript,figdiv=figdiv)    
