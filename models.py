import datetime
from copy import copy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True)

    @classmethod
    def find_or_create(cls, name):
        return cls.query.filter_by(name=name).first() or cls.get_or_none(name=name) or cls.create(name=name)


class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    opponent_id = db.Column('opponent_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    date = db.Column(db.Integer, nullable=False, index=True)
    school_score = db.Column(db.Integer, nullable=False)
    opponent_score = db.Column(db.Integer, nullable=False)

    school = relationship("School")
    opponent = relationship("School")

    @classmethod
    def find_or_create(cls, **kargs):
        new_args = copy(kargs)
        new_args['opponent'] = kargs['school']
        new_args['school'] = kargs['opponent']
        return cls.get_or_none(**kargs) or cls.get_or_none(**new_args) or cls.create(**kargs)


class GlickoRating(db.Model):
    __tablename__ = 'glicko_ratings'

    id = db.Column(db.Integer, primary_key=True)

    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    race_id = db.Column('races', db.Integer, db.ForeignKey("races.id"), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    school = relationship("School")
    race = relationship("Race")
