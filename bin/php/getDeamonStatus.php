<?

 $i = 0;
 foreach($cfg->bgp as $k => $v){
	$out = intval(exec("ps -ef | grep ".$v->lib." | grep -v grep | wc -l"));
	$d[$i]['id'] = $k;
	if($out > 0){
		$d[$i]['value'] = true;
	}
	else{
		$d[$i]['value'] = false;
	}
	
	$i++;
 }


header("Content-Type: application/json");
echo json_encode($d);
?>