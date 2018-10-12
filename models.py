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
        existing = cls.query.filter_by(name=name).first() or cls.query.filter_by(name=name).first()
        if existing:
            return existing
        else:
            new = cls(name=name)
            db.session.add(new)
            db.session.commit()
            return new


class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    opponent_id = db.Column('opponent_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    school_score = db.Column(db.Integer, nullable=False)
    opponent_score = db.Column(db.Integer, nullable=False)

    school = relationship("School", foreign_keys=[school_id])
    opponent = relationship("School", foreign_keys=[opponent_id])

    @classmethod
    def find_or_create(cls, **kargs):
        existing = cls.query.filter_by(**kargs).first()
        if existing:
            return existing
        else:
            new = cls(**kargs)
            db.session.add(new)
            db.session.commit()
            return new


class GlickoRating(db.Model):
    __tablename__ = 'glicko_ratings'

    id = db.Column(db.Integer, primary_key=True)

    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    race_id = db.Column('races', db.Integer, db.ForeignKey("races.id"), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    school = relationship("School")
    race = relationship("Race")
