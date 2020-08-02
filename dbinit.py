import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('walk.db')
    c = conn.cursor()
    c.execute('''
    create table Walk(
    ID int,
    Name varchar(255),
    Time TimeStamp default(datetime('now', 'localtime')),
    Point int
    )
    ''')
