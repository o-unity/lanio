<?
 //echo "<pre>";
 $loadObj = $_REQUEST["obj"];
 $loadObjRaw = $loadObj;
 if(!$loadObj){
  echo "no obj defined, terminate...";
  exit;
 }

 $loadObj = "win_".$loadObj;
 if(!isset($cfg->winStruct->$loadObj)){
 	$structLoad = "etc/conf/".$loadStruct."_config.php";
 	include($structLoad);
 	
 	$found = false;
 	foreach($winConfig as $k => $v){
 		if($v['id'] == $loadObj){
 			$found = true;
 			break;
 		}
 	}
 	if(!$found){
  		echo "windows config not found, terminate...";
  		exit;
 	}
 
 	if(!isset($cfg)){
 	  $cfg = new stdClass();	
 	} 	
 	if(!isset($cfg->winStruct)){
 	  $cfg->winStruct = new stdClass();	
 	}
 	$cfg->winStruct->$loadObj = new stdClass();
 	foreach($v as $k2 => $v2){
 		$cfg->winStruct->$loadObj->$k2 = new stdClass();
 		$cfg->winStruct->$loadObj->$k2 = $v2;
 	}
 	
 	//print_r($cfg);
 	//echo json_encode($cfg->winStruct->$loadObj,JSON_UNESCAPED_UNICODE);
 	//exit;
 }

 if(!isset($cfg->winStruct->$loadObj)){
  	echo "could not create object, terminate...";
  	exit;
 }
 
 $cfg->winStruct->$loadObj->buttonId = $loadObjRaw;
 
 header("Content-Type: application/json");
 echo json_encode($cfg->winStruct->$loadObj);


//array_merge_recursive(

?>