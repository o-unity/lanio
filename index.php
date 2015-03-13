<?
 $loadStruct = $_REQUEST["l"];
 $structLoad = "bin/".$loadStruct.".php";
 
 $configFile = "etc/conf/global.json";
 
 if($loadStruct){
	 if(file_exists($structLoad)){
	 	
	 	// CONFIG
	 	if(file_exists($structLoad)){
	 		$cfgJsonStr = file_get_contents($configFile);
	 		$cfg = json_decode($cfgJsonStr);
	 		$cfg_md5 = md5($cfgJsonStr);
	 	}
	 	else{
	 		echo "<b>config not found:</b> [$configFile]";
	 	}
	 	
	 	
	 	
	   include_once($structLoad);
	 }
	 else{
	 	echo "<b>file not found: [$structLoad]</b>";
	 }
	 
	 
	 /// DESTRUCT
	 $cfgJsonStr = json_encode($cfg);
	 if($cfgJsonStr == "null"){
	 	$cfgJsonStr = "";
	 }
	 if(md5($cfgJsonStr) != $cfg_md5){
	 	file_put_contents($configFile,$cfgJsonStr);
	 	//echo "write down new config";
	 }
 }
	
// LOAD INDEX IF NO STRUCT IS DEFINED
 if(!$loadStruct){
 	
?>
<!DOCTYPE html>
<html>
<head>
	<title>ebrixx - lanio configuration</title>
	<meta name="viewport" content="width=device-width, initial-scale=1"/>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
	<link rel="stylesheet" type="text/css" href="ext/dhtmlx/codebase/dhtmlx.css"/>
	<link rel="stylesheet" type="text/css" href="ext/src/lanio.css"/>
	<script src="ext/dhtmlx/codebase/dhtmlx.js"></script>
	<script src="ext/src/lanio.js"></script>

</head>
<body onload="doOnLoad();">
	<div id="my_logo" class="my_hdr"><div class="text"><img src="ext/img/ebrixx.png" align="right" height="70px"></div></div>
	
	<div id="treeboxbox_tree"></div>
	<div id="workspace" style="padding:20px"><div id="myForm"></div></div>
	<div id="accObj"></div>
	<div id="config" style="padding:20px"></div>
	<div id="toolbarObj"></div>
	<div id="winVP"></div>
	
</body>
</html>
<?
	}
?>