from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from apps import db, login_manager
from apps.waste_management import blueprint
from apps.waste_management.models import WasteType
from apps.waste_management.forms import WasteTypeForm


@blueprint.route('/waste_type', methods=['GET', 'POST'])
@login_required
def create_waste_type():
    # if current_user.role.value != 'admin':
    #     return jsonify({'error': 'Unauthorized access'}), 403

    form = WasteTypeForm()
    if form.validate_on_submit():
        waste_type = WasteType(
            name=form.name.data,
            description=form.description.data,
        )
        db.session.add(waste_type)
        db.session.commit()
        return jsonify({'message': 'Waste type created successfully'}), 201

    return render_template('create_waste_type.html', form=form)


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
