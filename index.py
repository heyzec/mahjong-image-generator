from io import BytesIO

from flask import Flask, request, send_file
from werkzeug import exceptions
from waitress import serve
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET'])
def result():
    if 'q' not in request.args:
        raise exceptions.BadRequest("Please specify mahjong hand in the parameter q.")

    q = request.args['q']
    if q == "":
        raise exceptions.BadRequest("The hand is empty!")

    output = []
    temp = []

    for i in range(len(q)):
        if q[i].isdigit():
            temp.append(q[i])
        elif q[i] in "mpsz":
            for ch in temp:
                output.append(ch + q[i])
            temp = []
        else:
            raise exceptions.BadRequest(f"The queried hand contains an unrecognised character: {q[i]}")

    imgs = []
    for tile in output:
        filename = f"tiles/{tile}.png"
        imgs.append(Image.open(filename))

    total_width = sum(map(lambda img: img.size[0], imgs))
    max_height = max(map(lambda img: img.size[1], imgs))

    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in imgs:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
