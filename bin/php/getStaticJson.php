<?
$winID 	= $_REQUEST["winID"];
$file 	= "etc/staticjson/".$winID.".json";
if(file_exists($file)){
	header("Content-Type: application/json");
	echo file_get_contents($file);
}
?>