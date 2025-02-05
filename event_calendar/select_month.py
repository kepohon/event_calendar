import sqlite3

conn = sqlite3.connect( 'memo.db' )
cur = conn.cursor()

print("何月？:", end="")
month = input()
int_month = int(month)

results = cur.execute(f"select * from daily where month={int_month} order by year, month, day")

print("要素数:", len(list(results)))

for row in cur.execute(f"select * from daily where month={int_month} order by year, month, day"):
    print(row)

conn.close()

