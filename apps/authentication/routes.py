from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, UpdateProfileForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass


# Login & Registration
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))
            # return redirect(url_for('authentication_blueprint.route_default'))

        return render_template(
            'authentication/login.html',
            msg='Wrong user or password',
            form=login_form
        )

    if not current_user.is_authenticated:
        return render_template('authentication/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template(
                'authentication/register.html',
                msg='Username already registered',
                success=False,
                form=create_account_form
            )

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template(
                'authentication/register.html',
                msg='Email already registered',
                success=False,
                form=create_account_form
            )

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template(
            'authentication/register.html',
            msg='Account created successfully.',
            success=True,
            form=create_account_form
        )

    else:
        return render_template('authentication/register.html', form=create_account_form)


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip_code = form.zip_code.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('authentication_blueprint.profile'))

    segment = get_segment(request)
    return render_template(
        'dashboard/profile.html',
        segment=segment,
        current_user=current_user,
        form=form
    )


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


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
