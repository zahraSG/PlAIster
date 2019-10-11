from flask import Blueprint, render_template, request
from dashboard.models import Postdevice
from dashboard.plots.routes import validList

main = Blueprint('main',__name__)


@main.route('/home') # these both will go to home
def home():
    page= request.args.get('page', 1, type = int)
    posts = Postdevice.query.order_by(Postdevice.crownID.asc()).paginate(per_page = 10, page=page) # get all devices added as posts and order by crownID and post the detials of each 10 devices in one page
    postnumber=len(Postdevice.query.all())
    return render_template('home.html',posts=posts, postnumber=postnumber)

@main.route('/')
@main.route('/about')
def about():
    Devicelist=validList()  # valid mac adresses ( adresses form the posted devices)
    length=len(Devicelist["device_list_posted"])
    return render_template('about.html',Devicelist=Devicelist, length=length)
