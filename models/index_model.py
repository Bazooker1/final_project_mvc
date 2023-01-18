import pandas

def get_student(conn):
    return pandas.read_sql(
        '''SELECT * FROM students
''', conn)

def get_activities(conn):
    return pandas.read_sql(
        '''SELECT * FROM activities
''', conn)

def get_group(conn):
    return pandas.read_sql(
        '''SELECT * FROM students_group
''', conn)

def insert_new_activity(conn, student_id, activity_id, role_id, end_date, start_date):
    cur = conn.cursor()

    cur.execute('''
INSERT INTO students_has_activities (id_activities, id_students, id_role, start_date, end_date)
VALUES (:activity_id, :student_id, :role_id, :start_date, :end_date);

    ''', {"activity_id": activity_id, "student_id": student_id, "role_id": role_id, "start_date": start_date, "end_date": end_date})

    conn.commit()

    return cur.lastrowid

def get_student_has_activities(conn, id_students):
    return pandas.read_sql('''
    SELECT activity_name AS Название, 
           activity_type_name AS Тип_мероприятия,
           role_name AS Роль,
           start_date AS Дата_начала,
           end_date AS Дата_окончания,
           student_has_activities_id 
    FROM students_has_activities
    JOIN activities USING (id_activities)
    JOIN activity_type USING (id_activity_type)
    JOIN students USING (id_students)
    JOIN role USING(id_role)
    WHERE students.id_students = :id
    ORDER BY id_students
    ''', conn, params={"id": id_students})


def get_activities_has_student(conn, id_activities):
    return pandas.read_sql('''
    SELECT fio AS ФИО_студента,
           role_name AS Роль
    FROM students_has_activities
    JOIN activities USING (id_activities)
    JOIN students USING (id_students)
    JOIN role USING(id_role)
    WHERE activities.id_activities = :id
    ORDER BY id_activities
    ''', conn, params={"id": id_activities})


def get_new_student(conn, new_student, new_id_group):
    cur = conn.cursor()

    cur.execute('''
INSERT INTO students(fio, id_group) VALUES (:new_student, :new_id_group)
    ''', {"new_student": new_student, "new_id_group": new_id_group})

    conn.commit()

    return cur.lastrowid


def end_activity(conn, student_has_activities_id):
    cur = conn.cursor()

    cur.executescript(f'''
UPDATE students_has_activities
SET end_date = date('now')
WHERE student_has_activities_id = {student_has_activities_id}
    ''')

    return conn.commit()