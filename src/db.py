import sqlite3

conn = sqlite3.connect('university.db')

def CreateTable():
    # subjects 테이블 생성
    conn.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        college TEXT,
        department TEXT,
        subject_type TEXT,
        subject_name TEXT,
        subject_code TEXT PRIMARY KEY,
        credits FLOAT,
        professor TEXT,
        time_1 TEXT,
        time_2 TEXT,
        classroom TEXT
        term INTEGER,
    )
    ''')

def InsertSampleData():
    # 샘플 데이터
    sample_subjects = []

    # 기존 데이터 삭제 후 새로운 데이터 삽입
    conn.executemany('INSERT INTO subjects VALUES (?,?,?,?,?,?,?,?,?,?)', sample_subjects)
    # 변경사항 저장
    conn.commit()
    conn.close()


def GetSubjects():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subjects')
    subjects = cursor.fetchall()
    conn.close()
    return subjects

if __name__ == "__main__":
    pass
