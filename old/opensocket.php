<?
/*
 $status = $_REQUEST["status"];
 if($status != "on"){
 	$status = "off";
 }
 */
 
$data = '{"api": {"input1":{"value":0}}}';
 
$fp = fsockopen("lanio", 50008, $errno, $errstr, 30);
if (!$fp) {
    echo "$errstr ($errno)<br />\n";
} else {
    fwrite($fp, $data."\r\n");
    while (!feof($fp)) {
        echo fgets($fp, 128);
    }
    fclose($fp);
}
?>