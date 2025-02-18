from flask import Blueprint

# Define the blueprint
main = Blueprint('main', __name__)

# Add routes to the blueprint
@main.route('/')
def home():
    return "Welcome to UniVerse!"
