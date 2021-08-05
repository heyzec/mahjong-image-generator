<?php

// A script botched together to show image of a certain mahjong hand.

$q = $_GET['q'];
function mergeImages($img1_path, $img2_path) {
	list($img1_width, $img1_height) = getimagesize($img1_path);
	list($img2_width, $img2_height) = getimagesize($img2_path);


	$merged_width  = $img1_width + $img2_width;
	//get highest
	$merged_height = $img1_height > $img2_height ? $img1_height : $img2_height;

	echo $merged_width . $merged_height;

	$merged_image = imagecreatetruecolor($merged_width, $merged_height);

	imagealphablending($merged_image, false);
	imagesavealpha($merged_image, true);

	$img1 = imagecreatefrompng($img1_path);
	$img2 = imagecreatefrompng($img2_path);

	imagecopy($merged_image, $img1, 0, 0, 0, 0, $img1_width, $img1_height);
	//place at right side of $img1
	imagecopy($merged_image, $img2, $img1_width, 0, 0, 0, $img2_width, $img2_height);

	//save file or output to broswer
	$SAVE_AS_FILE = TRUE;
	if( $SAVE_AS_FILE ){
	    $save_path = "temp.png";
	    imagepng($merged_image,$save_path);
	}

	//release memory
	imagedestroy($merged_image);
}

$output = array();
$temp = array();

for ($i = 0; $i < strlen($q); $i++) {
	if (is_numeric($q[$i])) {
		$temp[] = $q[$i];
	} else if (strpos('mpsz', $q[$i]) !== false) {
		foreach ($temp as $j) {
			$output[] = $j . $q[$i];
		}
		$temp = array();
	} else {
		echo "ERROR";
	}
}


print_r($output);
$firstRun = true;
foreach ($output as $tile) {
	$filename = "tiles/".$tile.".png";
	if ($firstRun) {
		copy($filename, "temp.png");
		$firstRun = false;
	} else {
		mergeImages("temp.png", $filename);
	}
}

echo header('Location: '.'temp.png');


?>
