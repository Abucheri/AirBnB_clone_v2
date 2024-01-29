#!/usr/bin/python3
"""Script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Display a HTML page with a list of all State objects."""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """Display a HTML page with a State's information and
    linked City objects.
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
