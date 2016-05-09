import pandas
from app import db
from app.models import Transportation,TransformedData

def get_data():
    # Load all data from database to be used by subsequent views
    raw_data = Transportation.query.with_entities(Transportation.stop_id,
                                              Transportation.on_street,
                                              Transportation.cross_street,
                                              Transportation.routes,
                                              Transportation.boardings,
                                              Transportation.alightings,
                                              Transportation.month_beginning,
                                              Transportation.daytype,
                                              Transportation.location).all()
    # Create pandas dataframe
    orig_df = pandas.DataFrame(raw_data,columns=['stop_id','on_street','cross_street','routes',
                               'boardings','alightings','month_beginning','daytype','location'])
    
    return orig_df

def get_transformed_data():
    # Load all data from database to be used by subsequent views
    raw_data = TransformedData.query.with_entities(TransformedData.stop_id,
                                              TransformedData.on_street,
                                              TransformedData.cross_street,
                                              TransformedData.routes,
                                              TransformedData.boardings,
                                              TransformedData.alightings,
                                              TransformedData.month_beginning,
                                              TransformedData.daytype,
                                              TransformedData.location,
                                              TransformedData.lat,
                                              TransformedData.lon,
                                              TransformedData.num_routes,
                                              TransformedData.route,
                                              TransformedData.total_traffic).all()

    # Create pandas dataframe
    df = pandas.DataFrame(raw_data,columns=['stop_id','on_street','cross_street','routes',
                               'boardings','alightings','month_beginning','daytype','location',
                                'lat','lon','num_routes','route','total_traffic'])
    
    return df

def create_dataframe(dataframe):
    orig_df = dataframe    
    # Sort dataframe by stop_id and fill NaN values
    df = orig_df.sort_values(by=['stop_id'])
    df = df.fillna('None')

    # Insert columns if they don't exist
    try:
        df.insert(len(df.columns),'lat', None)
        df.insert(len(df.columns),'lon', None)
        df.insert(len(df.columns),'route',None)
        df.insert(len(df.columns),'num_routes', None)
        df.insert(len(df.columns),'total_traffic', None)

    except: pass
    
    # Loop through dataframe and insert values for additional columns
    drop_ids = []
    for i,row in df.iterrows():
        # Create row for each route/stop. Remove old row.
        routes = str(row['routes']).split(',')
        coords = row['location'].split(',')
        lat,lon = coords[0].strip('('),coords[1].strip(')')
        total_traffic = float(row['boardings'])+float(row['alightings'])
        
        if len(routes)> 1:
            drop_ids.append(i)
            for route in routes:
                row['route'] = route
                row['lat'] = lat
                row['lon'] = lon
                row['total_traffic'] = total_traffic
                row['num_routes'] = len(routes)
                df.loc[len(df)+1] = row
        else:
            df.loc[i,'route'] = routes[0]
            df.loc[i,'lat'] = float(lat)
            df.loc[i,'lon'] = float(lon)
            df.loc[i,'total_traffic'] = total_traffic
            df.loc[i,'num_routes'] = len(routes)

    cleaned_df = df[~df.index.isin(drop_ids)]

    return (cleaned_df)

def routes_with_most_stops(dataframe):
    list_dict = []
    df_grouped = dataframe.groupby(by=['route'])
    for name,group in df_grouped:
        stop_count = len(group.index)
        route_dict = {'route':name,'stop_count':stop_count}
        list_dict.append(route_dict)
    longest_route_df = pandas.DataFrame(list_dict,columns=['route','stop_count']).sort_values(by=['stop_count'],ascending=False)
    longest_route_name = longest_route_df[(longest_route_df.stop_count==longest_route_df.stop_count.max())]['route'].values[0]
    return (longest_route_name,longest_route_df)

def find_busiest_route(dataframe):
    group_my_df = dataframe.groupby('route')
    for route,group in group_my_df:
        
        total_traffic = group['total_traffic'].sum()
        print route,total_traffic

orig_df = get_data()
df = get_transformed_data()
copy_df = df.copy()

most_routes_df = copy_df[['stop_id','on_street','cross_street','num_routes']].drop_duplicates('stop_id').sort_values(by=['num_routes'],ascending=False)
longest_route_name,longest_route_df=routes_with_most_stops(df)

if __name__=='__main__':
    orig_df = get_data()
    df = get_transformed_data()
    #find_busiest_route(df)
    #df = create_dataframe(orig_df)
    #df.to_sql(TransformedData.__tablename__,con=db.engine,if_exists='append',index=False)
