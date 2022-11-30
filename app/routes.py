from flask import Blueprint, render_template, redirect
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
        curs = conn.cursor()
        if form.validate_on_submit():
            new_appt = (
                form.name.data,
                datetime.combine(form.start_date.data, form.start_time.data),
                datetime.combine(form.end_date.data, form.end_time.data),
                form.description.data,
                form.private.data
            )

            sql = """INSERT INTO appointments (name, start_datetime, end_datetime, description, private) 
                    VALUES (?, ?, ?, ?, ?)
                    """
            curs.execute(sql, new_appt)
            # return redirect("/")
        
    today = datetime.now()
    return redirect(f"/{today.year}/{today.month}/{today.day}")


@bp.route("/<year>/<month>/<day>", methods=['POST','GET'])
def daily(year, month, day):
    with sqlite3.connect(DB_FILE) as conn:
        form = AppointmentForm()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()

        date_string = f"{year}-{month}-{day}"
        print(date_string)

        curs.execute("""SELECT * FROM appointments
                        WHERE DATE(start_datetime) = DATE(?)
                        """, (date_string, ))

        appointments = [dict(row) for row in curs.fetchall()]
        for appointment in appointments:

            appointment["start_datetime"] = datetime.strptime(
                appointment["start_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")

            appointment["end_datetime"] = datetime.strptime(
                appointment["end_datetime"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")
        times = [
            ('first time', '8 AM'), 
            ('middle time', '9 AM'), 
            ('middle time', '10 AM'), 
            ('middle time', '11 AM'), 
            ('middle time', '12 AM'), 
            ('middle time', '1 PM'), 
            ('middle time', '2 PM'), 
            ('middle time', '3 PM'), 
            ('middle time', '4 PM'), 
            ('middle time', '5 PM'), 
            ('middle time', '6 PM'), 
            ('middle time', '7 PM'), 
            ('last time', '8 PM')]
        return render_template("main.html", appointments=appointments, form=form, times=times)
