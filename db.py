from models import db, School, Race


if __name__ == '__main__':
    db.connect()
    db.create_tables([School, Race])
