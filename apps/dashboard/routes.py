from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from apps.dashboard import blueprint
from apps import login_manager


@blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    segment = get_segment(request)
    if current_user.role.value == 'user':
        template = 'dashboard/user_dashboard.html'
    elif current_user.role.value == 'wc_service':
        template = 'dashboard/wc_service_dashboard.html'
    elif current_user.role.value == 'admin':
        template = 'dashboard/admin_dashboard.html'
    else:
        flash('Role not recognized!', 'danger')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template(template, segment=segment)


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
