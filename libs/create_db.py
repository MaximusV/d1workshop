import sqlite3

DB_NAME = "high_score.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

schema = """
CREATE TABLE Score (
    name varchar(50) NOT NULL UNIQUE,
    score int NOT NULL
)
"""

index = "CREATE INDEX score_asc ON Score ('score' ASC)"

create = "INSERT INTO Score (name, score) VALUES ('test', 10)"

c.execute(schema)
c.execute(index)
c.execute(create)
conn.commit()
