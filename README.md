# PlAIster (Monitoring Power Usage)
## Dashboard for Monitoring Power Consumption
This dashboard visualizes the power usages messages from a Crownstone. check https://github.com/Mergon/crownstone-scanner for crownstone messages. The power usage of any number of devices connected to Crownstones existing in a Sphere can be visualized with this dashboard. It shows a live stream of power consumption.\

## Important Dependency:
This dashboard runs flask in the back-end which reads the database stored in CouchDB. Flask runs if and only if the CouchDB database receives data and then visualizes it on the front-end dashboard. 

## Dashboard Details:
The dashboard contains of the following tabs:\
**Home** ⇒  Home Contains a card for each device with the crownid and the macadress of the connected Crownstone. In this tab you can post or delect a device. \
**About** ⇒ A table of details of all devices with crownstone ID and macaddress.\
**Plots**  ⇒ A chart which shows the power usage of the last 10 minutes of all devices sending messages to our database (couchdb). The moving mean and median power usage of all devices are shown together with the current power usage.\
**Charts**   ⇒ In this tab a list of all devices is provided where we can select which devices do we want to see the live stream of the power usage.

## Required Packages
Make sure the following packages are installed with python3:
Flask \
Cloudant\
Numpy\
Pandas\
Json\
Datetime, time\
Plotly\
Flask_sqlalchemy\
For the live charts I used the vis.js javascript package : https://visjs.org/
