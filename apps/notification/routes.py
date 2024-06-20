from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.notification import blueprint
from apps.notification.models import Notification


@blueprint.route('/me/notifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    segment = get_segment(request)
    return render_template(
        'dashboard/notification.html',
        segment=segment,
        notifications=notifications
    )


@blueprint.route('/notifications/<int:id>/read', methods=['POST'])
@login_required
def mark_as_read(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    notification.read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked as read'})


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None


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