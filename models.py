from peewee import *
import datetime


db = SqliteDatabase('results.db')


class BaseModel(Model):
    class Meta:
        database = db


class School(BaseModel):
    name = CharField(unique=True, null=False)
    external_id = IntegerField(null=True)

    @classmethod
    def find_or_create(cls, name, external_id):
        school = cls.get_or_none(external_id=external_id) or cls(external_id=external_id)
        school.name = name
        school.save()
        return school


class Race(BaseModel):
    school_id = ForeignKeyField(School, backref='races')
    opponent_id = ForeignKeyField(School, backref='opponent_races')
    date = DateTimeField(default=datetime.datetime.now)
    school_score = IntegerField(null=False)
    opponent_score = IntegerField(null=False)

    @classmethod
    def find_or_create(cls, **kargs):
        return cls.get_or_none(**kargs) or cls.create(**kargs)
