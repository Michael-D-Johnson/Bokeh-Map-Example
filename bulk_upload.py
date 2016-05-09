#!/usr/bin/env python
import pandas
from app import db,models

table = models.Transportation.__tablename__

def bulk_upload(df,db,tablename):
    """ Take dataframe and insert into table"""
    df.to_sql(tablename,con=db.engine,if_exists='append',index=False)

csv_file = 'CTA_-_Ridership_-_Avg._Weekday_Bus_Stop_Boardings_in_October_2012.csv'
df = pandas.read_csv(csv_file)
df.fillna('NULL')

bulk_upload(df,db,table)
