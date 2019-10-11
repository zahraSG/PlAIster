from flask import Blueprint, render_template, url_for, flash, redirect, request
from dashboard import db
from dashboard.device.forms import  DeviceForm
from dashboard.models import Postdevice  # we have to import this after db to remove errors for importing db and reading from db which dose not exist yet

device = Blueprint('device',__name__)


@device.route('/device/new',methods=['GET','POST'])
def new_device():
    form = DeviceForm()
    if form.validate_on_submit():
        pp= Postdevice(name= form.name.data, crownID = form.crownID.data , macAddress= form.macAddress.data )
        db.session.add(pp)
        db.session.commit()
        flash ('Your device has ben added', 'success')
        return redirect(url_for('main.home'))
    return render_template ('create_device.html', title='New Device', form=form, legend='New Device')


@device.route('/device/<int:post_id>')
def detials(post_id):
    detials=Postdevice.query.get_or_404(post_id)
    return render_template('details.html', title= detials.name, post=detials)


@device.route('/device/<int:post_id>/update', methods=['GET','POST'])
def detials_update(post_id):
    update=Postdevice.query.get_or_404(post_id)
    form = DeviceForm()
    if form.validate_on_submit():
         update.name = form.name.data
         update.crownID= form.crownID.data
         update.macAddress = form.macAddress.data
         db.session.commit()
         flash("Your device is updated", "success")
         return redirect(url_for('device.detials',post_id=update.id))
    elif request.method == 'GET':
        form.name.data = update.name
        form.crownID.data = update.crownID
        form.macAddress.data = update.macAddress
    return render_template ('create_device.html', title='Update Device', form=form, legend='Update Device')


@device.route('/device/<int:post_id>/delete', methods=['POST'])
def delete_device (post_id):
    device=Postdevice.query.get_or_404(post_id)
    db.session.delete(device)
    db.session.commit()
    flash("The device has been deleted", "success")
    return redirect(url_for("main.home"))
