from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.recycling_tracker.models import RecyclingTracker
from apps.recycling_tracker.forms import RecyclingTrackerForm
from apps.notification.utils import create_notification
from apps.waste_management.models import WasteType
from apps.authentication.models import Users
from apps.recycling_tracker import blueprint


@blueprint.route('/recycling_tracker', methods=['GET', 'POST'])
@login_required
def create_recycling_tracker():
    if current_user.role.value != 'wc_service':
        return render_template('error/page-403.html'), 403

    form = RecyclingTrackerForm()

    # Populate the user choices
    form.user_id.choices = [(user.id, user.username)
                            for user in Users.query.all()]
    # Populate the waste type choices
    form.waste_type_id.choices = [
        (waste_type.id, waste_type.name) for waste_type in WasteType.query.all()]

    if form.validate_on_submit():
        waste_type = WasteType.query.get(form.waste_type_id.data)
        if not waste_type:
            return jsonify({'error': 'Invalid waste type ID'}), 400

        recycling_tracker = RecyclingTracker(
            user_id=form.user_id.data,
            service_id=current_user.id,
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
        create_notification(user_id=form.user_id.data,
                            message=notification_message)

    return render_template('dashboard/recycling_tracker_form.html', form=form)


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
