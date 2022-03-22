# Import the flask dependency
from flask import Flask

# Create new flask instance
app = Flask(__name__)

# Create the root route
@app.route('/')

def hellow_world():
    return 'Hello world!'