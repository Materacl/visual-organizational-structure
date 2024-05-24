from visual_organizational_structure.dashboards import bp

from flask import request, flash, redirect, url_for
from flask_login import login_required, current_user

from visual_organizational_structure.database import db
from visual_organizational_structure.models import User, Dashboard


@bp.route('/create_dashboard', methods=['POST'])
@login_required
def create_dashboard():
    name = request.form.get('name')
    if name:
        new_dashboard = Dashboard(name=name, user_id=current_user.id)
        db.session.add(new_dashboard)
        db.session.commit()

        return redirect(url_for('dashboards.view_dashboard', dashboard_id=new_dashboard.id))
    else:
        pass

    return redirect(url_for('main.home'))


@bp.route('/dashboard/<int:dashboard_id>')
@login_required
def view_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)

    if dashboard.user_id != current_user.id:
        return redirect(url_for('main.home'))

    return redirect(f'org-structure/{dashboard_id}')


@bp.route('/delete_dashboard/<int:dashboard_id>', methods=['POST'])
@login_required
def delete_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)

    if dashboard.user_id != current_user.id:
        return redirect(url_for("main.home"))

    db.session.delete(dashboard)
    db.session.commit()

    return redirect(url_for("main.home"))
