from io import BytesIO
import base64

from PIL import Image


def handle(event: dict, _):
    q = event['queryStringParameters']['q']

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
            raise Exception(f"The queried hand contains an unrecognised character: {ch}")

    imgs = []
    for tile in output:
        filename = f"tiles/{tile}.png"
        imgs.append(Image.open(filename))

    new_img = combine_imgs(imgs)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)

    # return send_file(img_io, mimetype='image/png')
    # return {
    #     'statusCode': 200,
    #     'body': img_io.read()
    # }
    return {
        'headers': { "Content-Type": "image/png" },
        'statusCode': 200,
        'body': base64.b64encode(img_io.read()).decode('utf-8'),
        'isBase64Encoded': True
    }

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

