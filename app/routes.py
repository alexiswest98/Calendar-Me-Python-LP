from flask import Blueprint, render_template
import os
import sqlite3
from datetime import datetime
from app.forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")


@bp.route("/")
def main():
    with sqlite3.connect(DB_FILE) as conn:
        form = AppointmentForm()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM appointments")
        appointments = [dict(row) for row in curs.fetchall()]
        for appointment in appointments:

            appointment["start_datetime"] = datetime.strptime(
                appointment["start_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")

            appointment["end_datetime"] = datetime.strptime(
                appointment["end_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")

        return render_template("main.html", appointments=appointments, form=form)
