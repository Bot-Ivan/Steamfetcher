
import flask
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
import requests
from requests.exceptions import JSONDecodeError
import main_functions
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_key(filename, api_name):
    api_key_dict = main_functions.read_from_file(filename)
    my_api_key = api_key_dict[api_name]
    return my_api_key

steam_api_key = get_key("steam_api.json","steam_key")
url = "https://api.steampowered.com"

#class to make the registration form for users to enter information
class UserInfo(FlaskForm):
    steamID = StringField("Username")
    submit = SubmitField('Submit')

def get_playersummaries_data(steam_api_key, parameter_entered):
    base_part = "https://api.steampowered.com/"
    interface_part = "ISteamUser/GetPlayerSummaries/v0002/"
    key = get_key("steam_api.json", "steam_key")
    key_part = "?key=" + key
    steam_id_part = "steamids=" + parameter_entered
    full_url = base_part + interface_part + key_part + steam_id_part

    try:
        response = requests.get(full_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Check if the response is not empty
        if response.text:
            data = response.json()
            persona_name = data['response']['players'][0]['personaname']
            return persona_name
        else:
            # Handle empty response
            print("Empty response received.")
            return None
    except JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserInfo()
    if request.method == "POST" and form.validate_on_submit():
        parameter_entered = form.steamID.data  # Change to steamID
        all_data = get_playersummaries_data(steam_api_key, parameter_entered)
        return render_template("userstats.html", data=all_data, form=form)
    return render_template("input_form.html", form=form)
    
if __name__ == "__main__":
    app.run(debug=True)