from io import BytesIO

from flask import Flask, request, send_file
from PIL import Image
from waitress import serve
from werkzeug import exceptions

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle():
    if 'q' not in request.args:
        raise exceptions.BadRequest("Please specify mahjong hand in the parameter q.")

    q = request.args['q']
    if q == "":
        raise exceptions.BadRequest("The hand is empty!")

    output = []
    temp = []

    for ch in q:
        if ch.isdigit():
            temp.append(ch)
        elif ch in "mpsz":
            for ch2 in temp:
                output.append(ch2 + ch)
            temp = []
        else:
            raise exceptions.BadRequest(f"The queried hand contains an unrecognised character: {ch}")

    imgs = []
    for tile in output:
        filename = f"tiles/{tile}.png"
        imgs.append(Image.open(filename))

    new_img = combine_imgs(imgs)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

def combine_imgs(imgs):
    """Concatenates multiple Images horizontally."""
    total_width = sum(map(lambda img: img.size[0], imgs))
    max_height = max(map(lambda img: img.size[1], imgs))

    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in imgs:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    return new_img



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
