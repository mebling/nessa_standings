from peewee import *
import datetime
from copy import copy

db = SqliteDatabase('results.db')


class BaseModel(Model):
    class Meta:
        database = db


class School(BaseModel):
    name = CharField(unique=True, null=False, index=True)

    @classmethod
    def find_or_create(cls, name):
        return cls.get_or_none(name=name) or cls.create(name=name)


class Race(BaseModel):
    school = ForeignKeyField(School, backref='races')
    opponent = ForeignKeyField(School, backref='opponent_races')
    date = IntegerField(null=False, index=True)
    school_score = IntegerField(null=False)
    opponent_score = IntegerField(null=False)

    @classmethod
    def find_or_create(cls, **kargs):
        new_args = copy(kargs)
        new_args['opponent'] = kargs['school']
        new_args['school'] = kargs['opponent']
        return cls.get_or_none(**kargs) or cls.get_or_none(**new_args) or cls.create(**kargs)


class GlickoRating(BaseModel):
    school = ForeignKeyField(School, backref="glicko_ratings", null=False)
    race = ForeignKeyField(Race, backref="glicko_ratings", null=False)
    rating = FloatField(null=False)
