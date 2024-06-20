from flask import jsonify, render_template
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.collection_route import blueprint
from apps.collection_route.models import CollectionRoute
from apps.collection_route.forms import CollectionRouteForm


@blueprint.route('/collection_route', methods=['POST'])
@login_required
def create_collection_route():
    if current_user.role != 'wc_service':
        return jsonify({'error': 'Unauthorized access'}), 403

    form = CollectionRouteForm()
    if form.validate_on_submit():
        collection_route = CollectionRoute(
            service_id=current_user.id,  # Assuming the current user is the service
            name=form.name.data,
            area=form.area.data,
            schedule=form.schedule.data
        )
        db.session.add(collection_route)
        db.session.commit()
        return jsonify({'message': 'Collection route created successfully'}), 201

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
