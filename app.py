import os

from flask import Flask, render_template, request, url_for
from models import *

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template('index.html', flights=flights)

@app.route("/book", methods=["POST"])
def book():
    '''Book a flight'''

    # Get form information
    name = request.form.get('name')
    try:
        flight_id = int(request.form.get('flight_id'))
    except ValueError:
        return render_template('error.html', message = 'Invalid Flight Number.')

    # make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template('error.html', message='No such flight with that id.')

    # add passengers
    flight.add_passenger(name)
    return render_template('success.html')


@app.route('/flights')
def flights() :
    # list all flights
    flights = Flight.query.all()
    return render_template("flights.html", title="Flights", flights=flights)

@app.route('/flights/<int:flight_id>')
def flight(flight_id) :
    """List deatails about a single flight."""
    # make sure a flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template('error.html', message='No such flight.')

    # get all passengers
    passengers = flight.passengers
    return render_template('flight.html', flight=flight, passengers=passengers)


if __name__ == '__main__':
    app.run(debug=True)
