Important:
Flask runs if and only if the back end runs which means if the couchdb runs it will have access to the live data and then visualize in a frontend dashboard. Otherwise it won't work

Dashboard Details:
For this dashboard I used flask in the backend and for front end I used html and javascript.

The dashboard contains of the following tabs:
Home ⇒ contains a card for each device with the crownid and the macadress of the connected crownstone. In this tab you can post or delect a device. This part is manual because the devices were part of 2 different spheres which I had access to only one sphere (Merry’s sphere). Therefore could not use the sphere tab which shows  the device list and can connect and read directly from the crownstone app sphere.

About ⇒ A table of all devices with crownstone ID and macaddress

Plots ⇒ a chart which shows the power usage of the last 10 minutes of all devices sending advertisements to our database (couchdb). The moving mean and median power usage of all devices are shown together with the current power usage.

Charts ⇒ In this tab we can select which devices do we want to see the live stream of power usage

Packages required to run the dashboard:
Make sure the following packages are insatalled with python - pip3:
Flask
Cloudant
Numpy
Pandas
Json
Datetime, time
Plotly
Flask_sqlalchemy

For the live charts I used the vis.js javascript package
