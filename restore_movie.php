<?php
$body = file_get_contents('php://input');
$submit = json_decode($body, true);

$frames_dataurl = $submit['data'];
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$extensions = [
    'image/gif' => 'gif',
    'image/jpeg' => 'jpg',
    'image/png' => 'png'
];

foreach($frames_dataurl as $frame_count => $datauri) {

  try {
    $data = str_replace(' ', '+' , $datauri);
    $data = preg_replace('#^data:image/\w+;base64,#i' , '' , $data);
    $data = base64_decode($data);
    $mime_type = finfo_buffer($finfo, $data);
  } catch (Exception $e) {
    echo "Decoding failure...";
    exit();
  }
  // echo $mime_type;

  if($mime_type == 'image/webp') {
    $filename = 'data/tmp/image' . sprintf("%05s", $frame_count) . ".webp";
    file_put_contents($filename, $data);
    $newfile = str_replace('webp', 'png', $filename);
    $convert = "ffmpeg -i " . $filename . " -vcodec png " . $newfile;
    exec($convert);
  } else {
    $filename = 'data/tmp/image' . sprintf("%05s", $frame_count) . ".png";
    file_put_contents($filename, $data);
  }

}

$generate = "ffmpeg -r 60 -i data/tmp/image%05d.png -vcodec libx264 -pix_fmt yuv420p -r 60 data/movie/" . $submit['label'] . ".mp4";
exec($generate);
$delete = "rm -f data/tmp/*";
exec($delete);

echo $submit['label'];

?>
