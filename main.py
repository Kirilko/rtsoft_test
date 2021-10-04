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
    data = read_csv()
    # args = [i.split('=')[1] for i in request.query_string.decode("utf-8").split('&')]
    args = request.args.getlist('category')
    images = []
    if args:  # изображения по указанным категориям
        for i in data:
            for j in args:
                if j in i[2:] and i[:2] not in images:
                    images.append(i[:2])
    else:  # произвольные изображения
        for i in data:
            images.append(i[:2])
    while images:
        rnd = 0
        if len(images) > 1:
            rnd = random.randint(0, len(images) - 1)
        cnt = int(images[rnd][1]) - 1
        if request.cookies.get(images[rnd][0]):
            cnt = int(request.cookies.get(images[rnd][0])) - 1
        if cnt < 0:
            images.pop(rnd)
            cnt = 0
        else:
            break
    image = ''
    if images:
        image = images[rnd][0]
    res = make_response(render_template('index.html', image=image, count=cnt,
                                        query=list(map(lambda x: f'category={x}', args))))
    if images:
        res.set_cookie(image, str(cnt))
    return res


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
