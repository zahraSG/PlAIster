from flask import Blueprint , render_template, request, flash, redirect, url_for
from dashboard import db
from dashboard.models import Postdevice
from matplotlib.figure import Figure
from cloudant.client import Cloudant
from cloudant.result import Result
import time
from datetime import datetime
import pandas as pd
import numpy as np
import json
# for view plot page
import plotly
import plotly.graph_objs as go


plots = Blueprint('plots',__name__)


user = "########"
password = "##############"
url="##################################"
link=(url % (user, password))
db_name = 'default' #'anne' #''default' #'peet' #'test'peet' #'test'default' #
ddoc_id = 'powerUsage'
view_id = 'byPiTimeAndID'
client=Cloudant(user, password, url=url, connect=True)
db = client.get(db_name, remote=True)
view = db.get_design_document(ddoc_id).get_view(view_id)


class datastore():
    device_names=[]
    device_ids=[]
    db_crownid=[]
    device_macaddress=[]
    db_macaddress=[]
    db_df=[]
    db_time =[]
    db_df=[]
    all_posts=[]
    time_view=[]
globaldata= datastore()


def get_data(start_time,selected_time):
    import time
    req_time =selected_time
    views=view( startkey=[str(req_time)], endkey=[str(start_time),{}], stale= 'update_after', stable = True, update ='lazy')['rows']
    keys=[result.get('key') for result in views]
    values=[result.get('value') for result in views]

    if len(keys) ==0 :
        flash ('No Data in this time', 'success')
        df=[]
        pattern = '%d.%m.%Y %H:%M:%S'
        start=time.strftime(pattern, time.localtime(start_time))
        end=time.strftime(pattern, time.localtime(req_time))
        raise TypeError ("No data is availble for this time between ", start, "and", end)
    else:
        dfkeys=pd.DataFrame(keys,columns=['localtimestamp', 'crownid', 'macAddress'])
        dfvalues=pd.DataFrame(values,columns=['powerUsage','LSB Timestamp'])
        df_all=pd.concat([dfkeys,dfvalues],axis=1)
        df_all['Datetime']=pd.to_datetime(df_all['localtimestamp'], unit='s', utc=True)
        df_all.set_index('Datetime', inplace=True)
        df_all.index = df_all.index.tz_convert('Europe/Amsterdam')
        validList()
        df = df_all.loc[np.isin(df_all['macAddress'].tolist() ,[globaldata.device_macaddress])]
        return (df)

@plots.route('/viewplot')
def viewplot():
    feature="Line"
    global globaldata
    post=Postdevice.query.all()
    globaldata.all_posts=post
    epoch_timenow = int(time.time())
    globaldata.time_view=epoch_timenow
    tt=epoch_timenow -600 # (10 minits)
    df=get_data(epoch_timenow,tt)
    print(df)
    globaldata.db_df=df
    pt=createPlot(feature,df)
    validList()
    print('plotly from ' ,epoch_timenow, " till  " , tt)
    return render_template('plots.html',plot=pt,feature= "Line" , posts=post , title='Plot last few seconds' )

def createPlot(feature,df):
        if feature =='Bar' :
            data=[go.Bar(x=df.index, y= pd.to_numeric(df['powerUsage']).tolist())]
            layout = go.Layout(showlegend=True, hovermode='closest')
            fig = go.Figure(data=data, layout=layout)
        elif feature =='Scatter'  :
            data=[go.Scatter(x=df.index, y= pd.to_numeric(df['powerUsage']).tolist(), mode = 'markers')]
            layout = go.Layout(showlegend=True, hovermode='closest')
            fig = go.Figure(data=data, layout=layout)
        else :
            data=[go.Scatter(x=df.index, y= pd.to_numeric(df['powerUsage']).tolist(), mode = 'markers+lines')]
            x =df.index
            y1 = pd.to_numeric(df['powerUsage']).tolist()
            y=[i/8 for i in y1]
            line_plt=go.Scatter(x=x, y=y, mode = 'markers+lines',marker=dict(color='blue'),name='linear-data')
            # moving median ( pd.rolling.meadian is good for timeseries data but if do can be done by np.convolve) check:  https://stackoverflow.com/questions/13728392/moving-average-or-running-mean

            df1 = df[['localtimestamp','powerUsage']]
            df1_median = df1.rolling(window=40, min_periods=2, center=True).median()
            y2=pd.to_numeric(df1_median['powerUsage']).tolist()
            y2=[i/8 for i in y2]
            median_plt=go.Scatter(x=x, y=y2,mode='markers+lines', line=dict(color='red', width=3),name='moving_median')

            # moving mean
            df1_mean = df1.rolling(window=40, min_periods=2, center=True).mean()
            y3=pd.to_numeric(df1_mean['powerUsage']).tolist()
            y3=[i/8 for i in y3]
            mean_plt=go.Scatter(x=x, y=y3,mode='markers+lines', line=dict(color='green', width=3),name='moving_mean')

            layout = go.Layout(
                showlegend=True,
                hovermode='closest',
                title=go.layout.Title(
                    text='Power usage in the last 10 minutes',
                    xref='paper',
                    x=0
                ),
                xaxis=go.layout.XAxis(
                    type= 'date',
                    title=go.layout.xaxis.Title(
                        text='Time is in GMT. Add 2 hours for local time',
                        font=dict(
                            size=18,
                            color='#7f7f7f')
                    )
                ),
                yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text='Watt',
                        font=dict(
                            size=18,
                            color='#7f7f7f')
                    )
                )
            )
            fig = go.Figure(data=[line_plt,median_plt, mean_plt], layout=layout)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return (graphJSON)


@plots.route('/validList')
def validList():
    device_list_posted = Postdevice.query.all()
    device_names = [p.name for p in device_list_posted]
    device_crownids = [p.crownID for p in device_list_posted]
    device_macaddress =  [a.lower() for a in[p.macAddress for p in device_list_posted]]
    globaldata.device_names = device_names
    globaldata.device_ids = device_crownids
    globaldata.device_macaddress =device_macaddress
    return {"device_list_posted" : device_list_posted,
            "device_macaddress":device_macaddress,
            "device_names": device_names,  "device_crownids":device_crownids}

@plots.route('/viewplot/<int:post_id>')
def device_plot(post_id):
    detials=Postdevice.query.get_or_404(post_id)
    print(detials)
    nn=detials.name
    crnid=detials.crownID
    mac=detials.macAddress

    df_all=globaldata.db_df
    if len(df_all) <1 :
        flash ('the data is updating', 'success')
        return redirect(url_for('plots.viewplot'))
    else:
        df_device = df_all.loc[(df_all['crownid']== crnid)  & np.isin(df_all['macAddress'].tolist() ,[globaldata.device_macaddress])]
        pt=createPlot(feature,df_device)
        return render_template('plot_device.html', title= detials.name, name=nn,crownid=crnid, plot=pt,posts=globaldata.all_posts)
