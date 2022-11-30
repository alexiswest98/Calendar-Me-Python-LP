from flask import Blueprint, render_template, redirect
import os
import sqlite3
from datetime import datetime
from app.forms import AppointmentForm


bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")


@bp.route("/", methods=['POST', 'GET'])
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


@bp.route("/<year>/<month>/<day>", methods=['POST', 'GET'])
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

        rows = [dict(row) for row in curs.fetchall()]

        appointments = {
            8:  {"class": 'first time', "time":  '8 AM', "appt": ''},
            9:  {"class": 'middle time', "time":  '9 AM', "appt": ''},
            10: {"class": 'middle time', "time": '10 AM', "appt": ''},
            11: {"class": 'middle time', "time": '11 AM', "appt": ''},
            12: {"class": 'middle time', "time": '12 AM', "appt": ''},
            13: {"class": 'middle time', "time":  '1 PM', "appt": ''},
            14: {"class": 'middle time', "time":  '2 PM', "appt": ''},
            15: {"class": 'middle time', "time":  '3 PM', "appt": ''},
            16: {"class": 'middle time', "time":  '4 PM', "appt": ''},
            17: {"class": 'middle time', "time":  '5 PM', "appt": ''},
            18: {"class": 'middle time', "time":  '6 PM', "appt": ''},
            19: {"class": 'middle time', "time":  '7 PM', "appt": ''},
            20: {"class": 'last time', "time":  '8 PM', "appt": ''}
        }

        for appointment in rows:

            start_datetime = datetime.strptime(
                appointment["start_datetime"], '%Y-%m-%d %H:%M:%S')
            appointment["start_datetime"] = start_datetime.strftime("%H:%M")

            end_datetime = datetime.strptime(
                appointment["end_datetime"], '%Y-%m-%d %H:%M:%S')
            appointment["end_datetime"] = end_datetime.strftime("%H:%M")

            military_time = start_datetime.hour

            appointments[military_time]["appt"] = appointment["name"]

        appointments = appointments.values()

        print("_"*50, appointments)

        return render_template("main.html", appointments=appointments, form=form)
