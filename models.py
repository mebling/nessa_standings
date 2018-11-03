import datetime
from copy import copy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()
NAME_MAPPINGS = {
  'Bishop Hendricken High School' : 'Bishop Hendricken HS',
  'Bishop Hendricken  HS': 'Bishop Hendricken HS',
  'Boston Latin School':'Boston Latin High School',
  'Portland HS':'Portland High School',
  "St. Sebastian's Country Day School":"St Sebastian's School",
  'Sturgis East Charter School':'Sturgis Charter School',
  'Swampscott High School':'Swampscott HS',
  'Valley Regional High School ':'Valley Regional High School',
  'Valley Regional High School \xa0':'Valley Regional High School'
}


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True)

    @classmethod
    def find_or_create(cls, name):
        name = NAME_MAPPINGS.get(name, name)
        existing = cls.query.filter_by(name=name).first()
        if existing:
            return existing
        else:
            new = cls(name=name)
            db.session.add(new)
            db.session.commit()
            return new


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)

    @classmethod
    def find_or_create(cls, year):
        existing = cls.query.filter_by(year=year).first()
        if existing:
            return existing
        else:
            new = cls(year=year)
            db.session.add(new)
            db.session.commit()
            return new


class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    opponent_id = db.Column('opponent_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)
    season_id = db.Column('season_id', db.Integer, db.ForeignKey("seasons.id"), nullable=False)

    date = db.Column(db.Date, nullable=False, index=True)
    school_score = db.Column(db.Integer, nullable=False)
    opponent_score = db.Column(db.Integer, nullable=False)

    school = relationship("School", foreign_keys=[school_id])
    opponent = relationship("School", foreign_keys=[opponent_id])
    season = relationship("Season", foreign_keys=[season_id], backref="races")

    @classmethod
    def find_or_create(cls, **kargs):
        existing = cls.query.filter_by(**kargs).first()
        new_args = copy(kargs)
        new_args['school_id'] = kargs['opponent_id']
        new_args['opponent_id'] = kargs['school_id']
        new_args['school_score'] = kargs['opponent_score']
        new_args['opponent_score'] = kargs['school_score']
        existing = existing or cls.query.filter_by(**new_args).first()
        if existing:
            return existing
        else:
            new = cls(**kargs)
            db.session.add(new)
            db.session.commit()
            return new


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column('school_id', db.Integer, db.ForeignKey("schools.id"), nullable=False)

    date = db.Column(db.Date, nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    rd = db.Column(db.Integer, nullable=False)

    school = relationship("School", foreign_keys=[school_id])
