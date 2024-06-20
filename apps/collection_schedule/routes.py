from flask import jsonify, render_template
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.collection_schedule import blueprint
from apps.collection_schedule.models import CollectionSchedule
from apps.collection_schedule.forms import CollectionScheduleForm
from apps.collection_route.models import CollectionRoute
from apps.notification.utils import create_notification


@blueprint.route('/collection_schedule', methods=['POST'])
@login_required
def create_collection_schedule():
    if current_user.role != 'user':
        return jsonify({'error': 'Unauthorized access'}), 403

    form = CollectionScheduleForm()
    if form.validate_on_submit():
        collection_route = CollectionRoute.query.get(form.route_id.data)
        if not collection_route:
            return jsonify({'error': 'Invalid route ID'}), 400

        collection_schedule = CollectionSchedule(
            user_id=current_user.id,
            route_id=form.route_id.data,
            date=form.date.data
        )
        db.session.add(collection_schedule)
        db.session.commit()

        # Create a notification for the wc_service
        message = f'New collection schedule created by user {current_user.username} for route {collection_route.name} on {form.date.data.strftime("%Y-%m-%d")}'
        create_notification(user_id=collection_route.service_id, message=message)

        return jsonify({'message': 'Collection schedule created successfully'}), 201

    return jsonify({'error': 'Invalid data'}), 400


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
