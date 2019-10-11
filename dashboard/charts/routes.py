from flask import Blueprint , render_template, request, flash, redirect, url_for
from dashboard.models import Postdevice
from dashboard.plots.routes import validList
from cloudant.client import Cloudant
from cloudant.result import Result
import time
import pandas as pd
import numpy as np
import json

# define the blueprint
charts = Blueprint('charts',__name__)


# # select the name of the database
#  DEVICESIN IN DIFFERENT DATABASES THAT WE CAN READ FROM
ANNE=['Anne - Ceiling lamp above dining table','Anne - Bedroom light','Anne - Main ceiling light','Anne - Crownstone Plug 22','Anne - Crownstone Plug 24','Anne - Crownstone Plug 28','Anne - Crownstone Plug 29','Anne - Crownstone Corner','Anne - Standing lamp','Anne - Guidestone Kitchen','Anne - Dishwasher']
PEET=['Audio Amplifier','Battery Charger','Charger','Coffee Maker (Senseo)','Digital TV Receiver','Freezer','Subwoofer','Tumble Dryer','USB-Hub','WiFi Router','Desktop Computer','Chandelier Dining Room','Vase Lamp']
DEFAULT=['Alarm Clock Radio','Bean-To-Cup Coffee Maker','Computer Printer','Dishwasher','Electrical Oven','Fridge & Freezer','Hair Dryer','Hair Straightener','Handmixer','Humidifier - Zahra','Immersion Blender','Iron','Juicer','Laptop Computer (Carolyns)','LCD Monitor (Carolyns)','Microwave','Nintendo Switch','Playstation 4','Toaster','Vacuum Cleaner','Washing Machine','Water Kettle','iMac','Philips Hue','Almende Humidifier','MacBook Pro (Meris)','Magimix (Andries)','LCD Monitor-Almende','dashboardpi3','Robert','Sandwich Maker','Induction Cooker','Egg Cooker','Big Brother','Beamer']


@charts.route("/chart")
def chart():
    alldevices=Postdevice.query.all()
    return render_template('charts.html',title='Monitor Power Usage', legend='Select a Device', alldevices=alldevices)


def getdatabase(db_name, start_time, req_time):
    user = "######"
    password = "######"
    url="################################"
    link=(url % (user, password))
    ddoc_id = 'powerUsage'
    view_id = 'byPiTimeAndID'

    client=Cloudant(user, password, url=url, connect=True)
    db    = client.get(db_name, remote=True)
    view  = db.get_design_document(ddoc_id).get_view(view_id)
    views = view( startkey=[str(req_time)], endkey=[str(start_time),{}], stale= 'update_after', stable = True, update ='lazy')['rows']
    keys  = [result.get('key') for result in views]
    values= [result.get('value') for result in views]

    if len(keys) ==0 :
        # flash ('No Data in this time', 'success')
        df=[]
        pattern = '%d.%m.%Y %H:%M:%S'
        start=time.strftime(pattern, time.localtime(start_time))
        end=time.strftime(pattern, time.localtime(req_time))
        print("No data is availble for this time between ", start, "and", end)
        # raise TypeError ("No data is availble for this time between ", start, "and", end)
    else:
        #flash ('Data exists for this time', 'success')
        dfkeys=pd.DataFrame(keys,columns=['localtimestamp', 'crownid', 'macAddress'])
        dfvalues=pd.DataFrame(values,columns=['powerUsage','LSB Timestamp'])
        df_all=pd.concat([dfkeys,dfvalues],axis=1)
        df_all['Datetime']=pd.to_datetime(df_all['localtimestamp'], unit='s', utc=True)
        df_all.set_index('Datetime', inplace=True)
        df_all.index = df_all.index.tz_convert('Europe/Amsterdam')
        Devicelist=validList()
        df = df_all.loc[np.isin(df_all['macAddress'].tolist() ,Devicelist["device_macaddress"])]
        return (df)


# get new data every time it is called by the vis chart in the charts.html file
@charts.route('/_update')
def update():
    # crownID, deviceName, macaddress are variables send by vis chart
    crownID=str(request.args.get('crownID', 0, type=int))
    deviceName=str(request.args.get('deviceName'));
    macaddress=str(request.args.get('macaddress'));
    macaddress=macaddress.lower()
    print('crown id is:' ,crownID,' for :', deviceName)
    timenow=int(time.time()) #curent moment

    # check which database the device is in
    if deviceName in DEFAULT:
        db_name = 'default'
    elif deviceName in PEET:
        db_name = 'peet'
    elif deviceName in ANNE:
        db_name = 'anne'

    df=getdatabase(db_name,timenow,timenow-10) # read database from 10 seconds ago till now
    if not isinstance(df, pd.DataFrame):
        print("no View created for this query")
        values_y='NaN'
        value_y= json.dumps(values_y)
        return value_y
    else :
        df_filtered= df.loc[(df['crownid'] == crownID) & (df['macAddress'] == macaddress) ].sort_values( "localtimestamp")
        df_filtered.drop_duplicates(inplace=True)
        values_y= pd.to_numeric(df_filtered['powerUsage']).tolist()
        # divide by eight
        values_y[:] = [x / 8 for x in values_y]
        values_x= json.dumps(pd.to_numeric(df_filtered['localtimestamp']).tolist())
        if values_y ==[]:
            print("no data availble")
            values_y='NaN'
            value_y= json.dumps(values_y)
            return value_y
        else:
            value_y=json.dumps(values_y[-1]) #get the last data to get the current time
            print("time is :   " , values_x)
            print("Power Usage IS:   ",value_y)
            return value_y
