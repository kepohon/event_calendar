import sqlite3

conn = sqlite3.connect( 'memo.db' )
cur = conn.cursor()

sql = "select * from daily order by year, month, day"
results = cur.execute( sql )
resultsCount = len(list(results))


for row in cur.execute( sql ):
    print(row)

print(f"results count: {resultsCount}")

conn.close()

