from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_group

@app.route('/new_student', methods=['get'])
def new_student():
    conn = get_db_connection()

    session['id_group'] = 0

    df_group = get_group(conn)

    html = render_template(
        'new_student.html',
        id_group=session['id_group'],
        combo_box=df_group,
        len=len
    )
    return html