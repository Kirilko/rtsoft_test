import random
from flask import Flask, request, render_template, make_response, redirect
import csv

app = Flask(__name__)


def read_csv():
    with open('test.csv', 'r') as file:
        reader = csv.reader(file, delimiter=";")
        data = []
        for row in reader:
            data.append(row)
        return data


@app.route("/", methods=['GET'])
def index():
    image_url_index = 0
    image_shows_amount_index = 1
    image_categories_index = 2
    min_images_len = 1

    csv_data = read_csv()
    categories = request.args.getlist('category')
    images_to_show = []
    if categories:
        for image in csv_data:
            for category in categories:
                if category in image[image_categories_index:] and image[:image_categories_index] not in images_to_show:
                    images_to_show.append(image[:image_categories_index])
    else:
        for image in csv_data:
            images_to_show.append(image[:image_categories_index])
    current_image = ''
    shows_count = 0
    while images_to_show:
        current_image_index = random.randint(0, len(images_to_show) - 1) if len(images_to_show) > min_images_len else 0
        shows_count = int(request.cookies.get(images_to_show[current_image_index][image_url_index],
                                              images_to_show[current_image_index][image_shows_amount_index]))
        current_image = images_to_show[current_image_index][image_url_index]
        shows_count -= 1
        if shows_count < 0:
            images_to_show.pop(current_image_index)
            shows_count = 0
            current_image = ''
        else:
            break
    response = make_response(render_template('index.html', image=current_image, count=shows_count,
                                             query=list(map(lambda x: f'category={x}', categories))))
    if images_to_show:
        response.set_cookie(current_image, str(shows_count))
    return response


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
