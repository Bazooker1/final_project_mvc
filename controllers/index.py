from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import insert_new_activity, get_student, get_student_has_activities, get_new_student, end_activity, get_group


@app.route('/', methods=['get'])
def index():
    isAdminLogged = False
    conn = get_db_connection()
    df_student = get_student(conn)
    df_group = get_group(conn)
    if request.values.get('exit_button'):
        session.clear()
        html = render_template(
            'login.html',
            len=len,
            combo_box=df_student,
            umik_box=df_group,
        )
        return html

    if session.get('admin'):
        isAdminLogged=True

    if (not request.values.get('admin') and not session.get('admin') and not session.get('id_students') and not request.values.get('student')):
        if (request.values.get('registration_button')):
            session['id_students'] = get_new_student(conn, request.values.get('new_fio'), request.values.get('group_id'))
        else:
            html = render_template(
                'login.html',
                len=len,
                combo_box=df_student,
                umik_box=df_group
            )
            return html
    elif request.values.get('admin'):
        session['id_students'] = 1
        session['admin'] = 1
        isAdminLogged = True
    elif request.values.get('student'):
        if session.get('admin'):
            session['admin'] = 1
            isAdminLogged = True
        id_students = int(request.values.get('student'))
        session['id_students'] = id_students
    elif request.values.get('new_student'):
        new_student = request.values.get('new_student')
        new_id_group = request.values.get('new_id_group')
        session['id_students'] = get_new_student(conn, new_student, new_id_group)
    elif request.values.get('noselect'):
        a = 1
    elif request.values.get('return'):
        student_has_activities_id = int(request.values.get('return'))
        end_activity(conn, student_has_activities_id)
    elif request.values.get('activity'):
        insert_new_activity(conn, session['id_students'], request.values.get('activity'), request.values.get('id_role'), request.values.get('end_date'), request.values.get('start_date'))
    else:
        session['id_students'] = 1

    df_student_has_activities = get_student_has_activities(conn, session['id_students'])
    df_student = get_student(conn)
    df_group = get_group(conn)

    # выводим форму
    html = render_template(
        'index.html',
        id_students=session['id_students'],
        combo_box=df_student,
        umik=df_group,
        student_has_activities=df_student_has_activities,
        len=len,
        isAdminLogged=isAdminLogged
    )
    return html