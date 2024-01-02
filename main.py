from flask import Flask, render_template, request
import requests
# from dotenv import load_dotenv
import os
# load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')

URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/original"
API_KEY = os.environ.get('API_KEY')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<type>', methods=['POST', 'GET'])
def search(type):
    if request.method == 'POST':
        query = request.form.get('query')
        parameters={
            'query':query,
            'api_key':API_KEY
        }
        try:
            response = requests.get(f'{URL}/search/{type}', params=parameters)
            if response.ok:
         
                data = response.json()['results']
                # print(data)
                return render_template('search.html', type=type, result=data, query=query)
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        except (KeyError, ValueError) as e:
            print(f"Error accessing JSON data: {e}")
    return render_template('search.html', type=type)

@app.route('/<type>/<int:id>/<title>')
def provider(type, id, title):
    data=None
    url = f'{URL}/{type}/{id}/watch/providers'
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ.get('AUTH_KEY')}"
}
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()['results']['IN']
            # print(data)

    except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
    except (KeyError, ValueError) as e:
            print(f"Error accessing JSON data: {e}")
    return render_template('provider.html', data=data, title=title)


if __name__ == '__main__':
    app.run(debug=False)