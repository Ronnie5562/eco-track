from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from apps.dashboard import blueprint
from apps import db, login_manager

from apps.authentication.models import Users
from apps.collection_route.models import CollectionRoute
from apps.collection_schedule.models import CollectionSchedule
from apps.recycling_tracker.models import RecyclingTracker
from apps.waste_management.models import WasteType


@blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    context = {}
    segment = get_segment(request)
    if current_user.role.value == 'user':
        template = 'dashboard/user_dashboard.html'

        results = RecyclingTracker.query.filter_by(
            user_id=current_user.id
        ).all()
        total_weight = sum([tracker.weight for tracker in results])

        context = {
            'waste_disposed_count': RecyclingTracker.query.filter_by(user_id=current_user.id).count(),
            'total_waste_recycled': total_weight,
            'waste_types': WasteType.query.count(),
            'my_recent_recycles': RecyclingTracker.query.filter_by(user_id=current_user.id).order_by(RecyclingTracker.date_collected.desc()).limit(5).all()
        }
    elif current_user.role.value == 'wc_service':
        template = 'dashboard/wc_service_dashboard.html'

        results = RecyclingTracker.query.filter_by(
            service_id=current_user.id
        ).all()
        total_weight = sum([tracker.weight for tracker in results])

        context = {
            'total_wastes_recycled': RecyclingTracker.query.filter_by(
                service_id=current_user.id
            ).count(),
            'total_waste_weight': total_weight,
            'number_of_waste_types': WasteType.query.count(),
            'recent_recycles': results
        }
    elif current_user.role.value == 'admin':
        template = 'dashboard/admin_dashboard.html'
        results = RecyclingTracker.query.all()
        total_weight = sum([tracker.weight for tracker in results])

        context = {
            'total_wastes_recycled': RecyclingTracker.query.count(),
            'total_waste_weight': total_weight,
            'number_of_waste_types': WasteType.query.count(),
            'list_of_all_users': list(Users.query.all())
        }
    else:
        flash('Role not recognized!', 'danger')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template(template, segment=segment, context=context)


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
