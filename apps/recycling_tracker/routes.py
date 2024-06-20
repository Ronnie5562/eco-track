from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.recycling_tracker import blueprint
from apps.recycling_tracker.models import RecyclingTracker
from apps.recycling_tracker.forms import RecyclingTrackerForm
from apps.notification.utils import create_notification
from apps.waste_management.models import WasteType


@blueprint.route('/recycling_tracker', methods=['POST'])
@login_required
def create_recycling_tracker():
    if current_user.role != 'wc_service':
        return jsonify({'error': 'Unauthorized access'}), 403

    form = RecyclingTrackerForm()
    if form.validate_on_submit():
        waste_type = WasteType.query.get(form.waste_type_id.data)
        if not waste_type:
            return jsonify({'error': 'Invalid waste type ID'}), 400

        recycling_tracker = RecyclingTracker(
            user_id=form.user_id.data,
            service_id=current_user.id,  # Assuming the current user is the service
            waste_type_id=form.waste_type_id.data,
            date_collected=form.date_collected.data,
            weight=form.weight.data
        )
        db.session.add(recycling_tracker)
        db.session.commit()

        # Create a notification for the user
        notification_message = (
            f'Your {waste_type.name} waste has been recycled by service {current_user.username} '
            f'on {form.date_collected.data.strftime("%Y-%m-%d")}. Weight: {form.weight.data} kg'
        )
        create_notification(
            user_id=form.user_id.data,
            message=notification_message
        )
        return jsonify({'message': 'Recycling tracker created successfully'}), 201

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
