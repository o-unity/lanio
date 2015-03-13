<?
	if(isset($cfg->winStruct)){
		foreach($cfg->winStruct as $k=>$v){
			if($cfg->winStruct->$k->active=="true"){
				$obj[]=array('id'=>$k,'buttonId'=>$cfg->winStruct->$k->buttonId);
			}
		}
	}
	header("Content-Type: application/json");
	echo json_encode($obj);
	
?>