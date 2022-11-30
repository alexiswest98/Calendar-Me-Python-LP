from flask import Blueprint, render_template
import os
import sqlite3
from datetime import datetime
from app.forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")


@bp.route("/", methods=['POST','GET'])
def main():
    with sqlite3.connect(DB_FILE) as conn:
        form = AppointmentForm()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        if form.validate_on_submit():
            new_appt = (
                form.name.data,
                datetime.combine(form.start_date.data, form.start_time.data),
                datetime.combine(form.end_date.data, form.end_time.data),
                form.description.data,
                form.private.data
            )

            sql = "INSERT INTO appointments (name, start_datetime, end_datetime, description, private) VALUES (?, ?, ?, ?, ?)"
            curs.execute(sql, new_appt)

        curs.execute("SELECT * FROM appointments")
        appointments = [dict(row) for row in curs.fetchall()]
        for appointment in appointments:

            appointment["start_datetime"] = datetime.strptime(
                appointment["start_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")

            appointment["end_datetime"] = datetime.strptime(
                appointment["end_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")

        return render_template("main.html", appointments=appointments, form=form)
