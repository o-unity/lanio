<?
/*
 $status = $_REQUEST["status"];
 if($status != "on"){
 	$status = "off";
 }
 */
 
 $status = "on";
 
$fp = fsockopen("localhost", 50008, $errno, $errstr, 30);
if (!$fp) {
    echo "$errstr ($errno)<br />\n";
} else {
    fwrite($fp, $status."\r\n");
    while (!feof($fp)) {
        echo fgets($fp, 128);
    }
    fclose($fp);
}
?>