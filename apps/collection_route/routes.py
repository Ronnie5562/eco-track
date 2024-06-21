from flask import jsonify, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.collection_route import blueprint
from apps.collection_route.models import CollectionRoute
from apps.collection_route.forms import CollectionRouteForm


@blueprint.route('/create_route', methods=['GET', 'POST'])
@login_required
def create_collection_route():
    if current_user.role.value != 'wc_service':
        return render_template('error/page-403.html'), 403

    form = CollectionRouteForm()
    if form.validate_on_submit():
        collection_route = CollectionRoute(
            service_id=current_user.id,
            name=form.name.data,
            area=form.area.data,
            schedule=form.schedule.data
        )
        db.session.add(collection_route)
        db.session.commit()
        return redirect(url_for('collection_route_blueprint.view_routes'))

    return render_template('dashboard/create_route.html', form=form)


@blueprint.route('/view_routes')
@login_required
def view_routes():
    if current_user.role.value != 'wc_service':
        return render_template('error/page-403.html'), 403

    routes = CollectionRoute.query.filter_by(service_id=current_user.id).all()
    return render_template('dashboard/view_routes.html', routes=routes)

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
