from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_activities_has_student, get_activities

@app.route('/activity', methods=['get'])
def activity():
    conn = get_db_connection()

    df_activities = get_activities(conn)
    df_activities_students = get_activities_has_student(conn, request.values.get('id_activities'))

    if request.values.get('id_activities'):
        id_activities = int(request.values.get('id_activities'))
        session['id_activities'] = id_activities
    else:
        session['id_activities'] = 0

    html = render_template(
        'activity.html',
        df_activities=df_activities,
        df_activities_students=df_activities_students,
        id_activities=session['id_activities'],
        len=len
    )
    return html