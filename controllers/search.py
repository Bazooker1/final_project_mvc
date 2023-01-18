from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_activity_type, get_role, card


@app.route('/search', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_activity_type = get_activity_type(conn)
    df_role = get_role(conn)

    if request.form.get('clear'):
        activity_types = []
        roles = []
    else:
        activity_types = [int(item) for item in request.form.getlist('id_activity_type')]
        roles = [int(item) for item in request.form.getlist('id_role')]

    df_card = card(conn, activity_types, roles)

    html = render_template(
        'search.html',
        roles=df_role,
        activity_types=df_activity_type,
        card=df_card,
        sel_roles=roles,
        sel_activity_types=activity_types,
        len=len
    )
    return html