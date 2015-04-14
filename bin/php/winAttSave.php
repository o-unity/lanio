<?
 //obj=win_configBP&postion=370,45
 $loadObj 	= $_REQUEST["obj"];
 $position 	= $_REQUEST["position"];
 $active 	= $_REQUEST["active"];
 
 $maxHeight = intval($_REQUEST["maxHeight"]);
 $maxWidth 	= intval($_REQUEST["maxWidth"]);

 $dimension = $_REQUEST["dimension"]; 
 
 
 $pos = explode(",",$position);
 $dim = explode(",",$dimension);
 
 $left 		= intval($pos[0]);
 $top  		= intval($pos[1]);
 if($left < 0){
 	$left = 0;
 }
 if($top < 0){
 	$top = 0;
 } 
 
 $winwidth 	= intval($dim[0]);
 $winheight  = intval($dim[1]); 
 
 if($left > ($maxWidth - (50 + $winwidth))){
 	$left = ($maxWidth - (50 + $winwidth));
 }
 if($top > ($maxHeight - (50 + $winheight))){
 	$top = ($maxHeight - (50 + $winheight));
 } 
 
 $cfg->winStruct->$loadObj->left 	= $left;
 $cfg->winStruct->$loadObj->top 	= $top;
 $cfg->winStruct->$loadObj->width 	= $winwidth;
 $cfg->winStruct->$loadObj->height 	= $winheight; 
 $cfg->winStruct->$loadObj->active 	= $active; 
 
 //echo $top." - ".$maxHeight." - ".($maxHeight - 50 - $winheight)."\n";
 //echo $left." - ".$maxWidth." - ".($maxWidth - 50 - $winwidth)."\n";
 
 header("Content-Type: application/json");
 echo '{status: "ok",test:"sssss"}';
?>