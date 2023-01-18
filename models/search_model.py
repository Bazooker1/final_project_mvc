import pandas as pd


def get_activity_type(conn):
    return pd.read_sql('''
        SELECT id_activity_type, activity_type_name, COUNT(activities.id_activities)
        FROM activity_type
        JOIN activities USING(id_activity_type)
        GROUP BY activity_type_name''', conn)


def get_role(conn):
    return pd.read_sql('''
        SELECT id_role, role_name, COUNT(a.id_activities)
        FROM role AS r
        JOIN students_has_activities AS sha USING(id_role)
        JOIN activities AS a WHERE sha.id_activities = a.id_activities
        GROUP BY role_name''', conn)


def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = ",".join(s)

    return res

def card(conn, activity_types, roles):
    activity_types = convert(activity_types)
    roles = convert(roles)
    return pd.read_sql(f'''
            SELECT
            	activity_name AS 'Название',
            	activity_type_name AS 'Тип_мероприятия',
            	start_date AS 'Дата_начала',
                end_date AS 'Дата_окончания',
                role_name AS 'Роли',
                r.id_role as 'Role_Id',
                id_activities AS 'ID'
            FROM activities AS a
            JOIN students_has_activities AS sha USING(id_activities)
            JOIN activity_type USING(id_activity_type)
            JOIN role AS r WHERE sha.id_role = r.id_role
            GROUP BY id_activities
            HAVING (r.id_role IN ({roles}) OR ({not roles}))
                AND (id_activity_type IN ({activity_types}) OR ({not activity_types}))
            ORDER BY
                activity_name,
                activity_type_name 
        ''', conn)