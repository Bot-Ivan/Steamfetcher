
import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import Flaskform
from wtforms import IntegerField, SubmitField, SelectField, validators
import os
from wtforms.validators import NumberRange
import main_functions
import requests

app = flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_key(filename, api_name):
    api_key_dict = main_functions.read_from_file(filename)
    my_api_key = api_key_dict[api_name]
    return my_api_key

steam_api_key = get_key("api_key.json","steam_key")
url = "https://api.steampowered.com"

#class to make the registration form for users to enter information
class Registration(Flaskform):
    pass
