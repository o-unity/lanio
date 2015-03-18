<?
$winID 	= $_REQUEST["winID"];
$uriR	= explode("?",$_SERVER["REQUEST_URI"]);
$uri	= $uriR[0];

$file 	= "ext/src/".$winID.".js";
if(file_exists($file)){
	include_once($file);
}
else{
?>	
function includejs_<? echo $winID ?>(){
	dhtmlx.message({
		type: "error",
		text: "upps, include not found [<? echo $file ?>]"
	});
}
includejs_<? echo $winID ?>();

<?	
}
?>

