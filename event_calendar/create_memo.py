import sqlite3

conn = sqlite3.connect( 'memo.db' )
cur = conn.cursor()

cur.execute("""create table if not exists daily (
                id integer primary key autoincrement,
                year integer,
                month integer,
                day integer,
                memo text not null);""")


#day = '2025_1_13'
year = 2025
month = 1
day = 14
memo = 'テニシュ'

sql = 'insert into daily(year, month, day, memo) values (?, ?, ?, ?)'
cur.execute(sql, (year, month, day, memo) )

conn.commit()

for row in cur.execute("select * from daily order by year, month, day"):
    print(row)

conn.close()

