import sqlite3

conn = sqlite3.connect( 'memo.db' )
cur = conn.cursor()

print("検索文字列: ", end="")
searchString = input()

sql = f"select * from daily where memo like '%{searchString}%' order by year, month, day;"

for row in cur.execute( sql ):
    print(row)

conn.close()

