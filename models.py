from venv import create
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class Show(db.Model):
    __table__name = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship('Show', backref='venue', lazy=True)

    @property
    def num_upcoming_shows(self):
        show_result = 0
        info = Venue.query.get(self.id).shows
        if info:
            for days in info:
                if days.created_date > datetime.utcnow().replace(tzinfo=pytz.UTC):
                    show_result += 1
        return show_result
    
    @property
    def num_past_shows(self):
        show_result = 0
        info = Venue.query.get(self.id).shows
        if info:
            for days in info:
                if days.created_date < datetime.utcnow().replace(tzinfo=pytz.UTC):
                    show_result += 1
        return show_result

    @property
    def past_shows(self):
        result = {}
        final_result = []
        info = Venue.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date < datetime.utcnow().replace(tzinfo=pytz.UTC):
                    result["artist_id"] = show.artist_id
                    result["artist_name"] = show.artist.id
                    result["artist_image_link"] = show.artist.image_link
                    result["start_time"] = str(show.created_date)
                final_result.append(result)
        return final_result

    @property
    def upcoming_shows(self):
        result = {}
        final_result = []
        info = Venue.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date > datetime.utcnow().replace(tzinfo=pytz.UTC):
                    result["artist_id"] = show.artist_id
                    result["artist_name"] = show.artist.id
                    result["artist_image_link"] = show.artist.image_link
                    result["start_time"] = str(show.created_date)
                final_result.append(result)
        return final_result


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
