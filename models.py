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
    __table__name = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Venue(db.Model):
    __tablename__ = 'venue'

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
                if days.created_date > datetime.now():
                    show_result += 1
        return show_result
    
    @property
    def num_past_shows(self):
        show_result = 0
        info = Venue.query.get(self.id).shows
        if info:
            for days in info:
                if days.created_date < datetime.now():
                    show_result += 1
        return show_result

    @property
    def past_shows(self):
        final_result = []
        info = Venue.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date < datetime.now():
                    final_result.append(
                        {
                            "artist_id": show.artist_id,
                            "artist_name": show.artist.id,
                            "artist_image_link": show.artist.image_link,
                            "start_time": str(show.created_date)
                        }
                    )
        return final_result

    @property
    def upcoming_shows(self):
        final_result = []
        info = Venue.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date > datetime.now():
                    final_result.append(
                        {
                            "artist_id": show.artist_id,
                            "artist_name": show.artist.id,
                            "artist_image_link": show.artist.image_link,
                            "start_time": str(show.created_date)
                        }
                    )
        return final_result


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship('Show', backref='artist', lazy=True)

    @property
    def num_upcoming_shows(self):
        show_result = 0
        info = Artist.query.get(self.id).shows
        if info:
            for days in info:
                if days.created_date > datetime.now():
                    show_result += 1
        return show_result
    
    @property
    def num_past_shows(self):
        show_result = 0
        info = Artist.query.get(self.id).shows
        if info:
            for days in info:
                if days.created_date < datetime.now():
                    show_result += 1
        return show_result

    @property
    def past_shows(self):
        final_result = []
        info = Artist.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date < datetime.now():
                    final_result.append(
                        {
                            "venue_id": show.venue_id,
                            "venue_name": show.venue.name,
                            "venue_image_link": show.venue.image_link,
                            "start_time": str(show.created_date)
                        }
                    )
      
        return final_result

    @property
    def upcoming_shows(self):
        final_result = []
        info = Artist.query.get(self.id).shows 
        if info:
            for show in info:
                if show.created_date > datetime.now():
                    final_result.append(
                        {
                            "venue_id": show.venue_id,
                            "venue_name": show.venue.name,
                            "venue_image_link": show.venue.image_link,
                            "start_time": str(show.created_date)
                        }
                    )
                 
        return final_result

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
