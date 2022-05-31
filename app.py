#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import re
from urllib import response
from wsgiref import validate
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from markupsafe import Markup
from  models import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.app = app

db.init_app(app)
Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  inner_data = {}

  try:
    info = Venue.query.filter().all()
    for datum in info:
      if datum.city not in inner_data:
        inner_data[datum.city] = {
          "city": datum.city,
          "state":datum.state,
          "venues": [
            {
              "id" : datum.id,
              "name" : datum.name,
              "num_upcoming_shows": Venue.query.get(datum.id).num_upcoming_shows
            }
          ]
        }
      else:
        inner_data[datum.city]["venues"].append( {
              "id" : datum.id,
              "name" : datum.name,
              "num_upcoming_shows": Venue.query.get(datum.id).num_upcoming_shows
            })
    for key in inner_data:
      data.append(inner_data[key])
    return render_template('pages/venues.html', areas=data)
  except:
    flash("No available venues yet")

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {
    'count': 0,
    'data': []
  }
  data = []
  search_term = request.form.get('search_term', '')
  filters = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  for item in filters:
        response['count'] = len(filters)
        response['data'].append({
          "id" : item.id,
          "name": item.name,
          "num_upcoming_shows": item.num_upcoming_shows
        })
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 
  data = {}
  try:
    venue = Venue.query.get(venue_id)
    
    data["id"] = venue.id
    data["genres"] = venue.genres
    data["address"] = venue.address
    data["city"] = venue.city
    data["state"] = venue.state
    data["phone"] = venue.phone
    data["website"] = venue.website_link
    data["facebook_link"] = venue.facebook_link
    data["seeking_talent"] = venue.seeking_talent
    data["seeking_description"] = venue.seeking_description
    data["image_link"] = venue.image_link
    data["past_shows"] = venue.past_shows
    data["upcoming_shows"] = venue.upcoming_shows
    data["past_shows_count"] = venue.num_past_shows
    data["upcoming_shows_count"] = venue.num_upcoming_shows
    
    return render_template('pages/show_venue.html', venue=data)
  except:
    flash('Venue does not exist' )
    return render_template('pages/show_venue.html', venue= data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  if form.validate_on_submit():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_talent = request.form.get('seeking_talent',  type=bool)
    seeking_description = request.form.get('seeking_description')

    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

  else:
      for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
          print(err)
      flash('Failed to create Venue ' + request.form['name'] )
      return render_template('forms/new_venue.html', form=form)
        

@app.route('/venues/<venue_id>/delete', methods=['DELETE', 'POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  db.session.delete(venue)
  db.session.commit()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  flash('Venue deleted successfully' )
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  try:
    data = Artist.query.filter().all()
  except:
    flash("No available artist yet")

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  response = {
    'count': 0,
    'data': []
  }
  data = []
  search_term = request.form.get('search_term', '')
  filters = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  for item in filters:
        response['count'] = len(filters)
        response['data'].append({
          "id" : item.id,
          "name": item.name,
          "num_upcoming_shows": item.num_upcoming_shows
        })
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = {}
  try:
    artist = Artist.query.get(artist_id)
    data["id"] = artist.id
    data["name"] = artist.name
    data["genres"] = artist.genres
    data["city"] = artist.city
    data["state"] = artist.state
    data["phone"] = artist.phone
    data["website"] = artist.website_link
    data["facebook_link"] = artist.facebook_link
    data["seeking_venue"] = artist.seeking_venue
    data["seeking_description"] = artist.seeking_description
    data["image_link"] = artist.image_link
    data["past_shows"] = artist.past_shows
    data["upcoming_shows"] = artist.upcoming_shows
    data["past_shows_count"] = artist.num_past_shows
    data["upcoming_shows_count"] = artist.num_upcoming_shows
    return render_template('pages/show_artist.html', artist=data)
  except Exception as e:
    print(e)
    flash('Artist does not exist' )

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data = Artist.query.get(artist_id)
  artist = {
    "id": artist_data.id,
    "name": artist_data.name,
    "genres": artist_data.genres,
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    "website": artist_data.website_link,
    "facebook_link": artist_data.facebook_link,
    "seeking_venue": artist_data.seeking_venue,
    "seeking_description": artist_data.seeking_description,
    "image_link": artist_data.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  get_artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_venue = request.form.get('seeking_talent',  type=bool)
    seeking_description = request.form.get('seeking_description')

    get_artist.name = name
    get_artist.city = city
    get_artist.state = state
    get_artist.phone = phone
    get_artist.image_link = image_link
    get_artist.genres = genres
    get_artist.facebook_link = facebook_link
    get_artist.website_link = website_link
    get_artist.seeking_venue = seeking_venue
    get_artist.seeking_description = seeking_description

    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))

  for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        print(err)

  flash('Artist ' + request.form['name'] + ' was not updated!')
  return render_template('forms/edit_artist.html', form=form, artist=get_artist)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_data = Venue.query.get(venue_id)
  venue = {
    "id": venue_data.id,
    "name": venue_data.name,
    "genres": venue_data.genres,
    "address": venue_data.address,
    "city": venue_data.city,
    "state": venue_data.state,
    "phone":venue_data.phone,
    "website": venue_data.website_link,
    "facebook_link": venue_data.facebook_link,
    "seeking_talent": True,
    "seeking_description": venue_data.seeking_description,
    "image_link": venue_data.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  get_venue = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  if form.validate_on_submit():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_talent = request.form.get('seeking_talent',  type=bool)
    seeking_description = request.form.get('seeking_description')

    # venue record with ID <venue_id> using the new attributes
    get_venue.name = name
    get_venue.city = city
    get_venue.state = state
    get_venue.address = address
    get_venue.phone = phone
    get_venue.image_link = image_link
    get_venue.genres = genres
    get_venue.facebook_link = facebook_link
    get_venue.website_link = website_link
    get_venue.seeking_talent = seeking_talent
    get_venue.seeking_description = seeking_description

    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))
  
  for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        print(err)
  flash('Venue ' + request.form['name'] + ' was not successfully updated!')
  return render_template('forms/edit_venue.html', form=form, venue=get_venue)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)
  if form.validate_on_submit():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_venue = request.form.get('seeking_talent',  type=bool)
    seeking_description = request.form.get('seeking_description')

    artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
  else:
    for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        print(err)
    flash('Failed to create Artist ' + request.form['name'] )
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  inner_data = {}
  try:
    all_shows = Show.query.all()
    for show in all_shows:
      inner_data["venue_id"] = show.venue_id
      inner_data["venue_name"] = show.venue.name
      inner_data["artist_id"] = show.artist.id
      inner_data["artist_name"] = show.artist.name
      inner_data["artist_image_link"] = show.artist.image_link
      inner_data["start_time"] = str(show.created_date)
      data.append(inner_data)
  except:
    flash("No available shows yet")

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  if form.validate_on_submit():
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    # new_date = format_datetime(start_time)
    new_show  = Show(venue_id=venue_id, artist_id=artist_id, created_date=start_time)
    db.session.add(new_show)
    db.session.commit()
  else:
    for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        print(err)
    flash('Failed to create Show ' )
    return render_template('forms/new_show.html', form=form)


  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
