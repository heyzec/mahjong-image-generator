from flask import Flask, request, send_file
from PIL import Image
import shutil

app = Flask(__name__)

@app.route('/', methods=['GET'])
def result():
    q = request.args['q']
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
            raise Exception()

    first_run = True
    tempfile = "tempfile.png"
    for tile in output:
        filename = f"tiles/{tile}.png"
        if first_run:
            shutil.copyfile(filename, tempfile)
            first_run = False
        else:
            merge_images(tempfile, filename)

    return send_file(tempfile, mimetype='image/png')

def merge_images(filename1, filename2):
    img1, img2 = Image.open(filename1), Image.open(filename2)

    total_width = sum([img1.size[0], img2.size[0]])
    max_height = max([img1.size[1], img2.size[1]])

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    new_im.paste(img1, (x_offset, 0))
    new_im.paste(img2, (img1.size[0], 0))

    new_im.save(filename1)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

# for ($i = 0; $i < strlen($q); $i++) {
# 	if (is_numeric($q[$i])) {
# 		$temp[] = $q[$i];
# 	} else if (strpos('mpsz', $q[$i]) !== false) {
# 		foreach ($temp as $j) {
# 			$output[] = $j . $q[$i];
# 		}
# 		$temp = array();
# 	} else {
# 		echo "ERROR";
# 	}
# }


# $firstRun = true;
# foreach ($output as $tile) {
# 	$filename = "tiles/".$tile.".png";
# 	if ($firstRun) {
# 		copy($filename, "temp_".$q."png");
# 		$firstRun = false;
# 	} else {
# 		mergeImages("temp_".$q."png", $filename);
# 	}
# }



