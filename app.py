from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def get_random_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0]['url']
    else:
        return None

@app.route('/')
def index():
    cat_image_url = get_random_cat_image()
    return render_template('index.html', cat_image_url=cat_image_url)

@app.route('/new')
def new_image():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
