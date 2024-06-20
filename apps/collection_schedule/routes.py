# routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.collection_schedule import blueprint
from apps.collection_schedule.forms import CollectionScheduleForm
from apps.collection_schedule.models import CollectionSchedule
from apps.collection_route.models import CollectionRoute
from apps.notification.utils import create_notification


@blueprint.route('/schedule_collection', methods=['GET', 'POST'])
@login_required
def schedule_collection():
    form = CollectionScheduleForm()

    # Fetch routes from the database
    routes = CollectionRoute.query.all()
    form.route_id.choices = [(route.id, route.name) for route in routes]

    if form.validate_on_submit():
        collection_route = CollectionRoute.query.get(form.route_id.data)
        if not collection_route:
            flash('Invalid route ID', 'danger')
            return render_template('collection_schedule/schedule_collection.html', form=form)

        collection_schedule = CollectionSchedule(
            user_id=current_user.id,
            route_id=form.route_id.data,
            date=form.date.data
        )
        db.session.add(collection_schedule)
        db.session.commit()

        # Create a notification for the wc_service
        message = f'New collection schedule created by user {current_user.username} for route {collection_route.name} on {form.date.data.strftime("%Y-%m-%d")}'
        create_notification(
            user_id=collection_route.service_id, message=message)

        flash('Collection schedule created successfully', 'success')
        return redirect(url_for('collection_schedule_blueprint.schedule_collection'))

    return render_template('dashboard/schedule_collection.html', form=form)



# Error Pages
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500
