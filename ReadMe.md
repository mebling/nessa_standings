# db.py
We use flask and postgresql.  You can use `createdb nessa` to create the db.  To run the migrations you can run `flask db upgrade`.  You need the env variable DATABASE_URL to be set to `postgresql://localhost/nessa` or you can comment it out in app.py

# scrape.py
Run `python scrape.py` to insert the data into the database
