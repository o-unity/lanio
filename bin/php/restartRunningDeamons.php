<?

	echo "<pre>";
	$jsStr = file_get_contents("http://localhost?l=getDeamonStatus");
	$js = json_decode($jsStr);
	
	foreach($js as $k => $v){
		if($v->value){
			echo "stop ".$v->id;
			echo "\n";
			flush();
			echo file_get_contents("http://localhost?l=setDeamonStatus&name=".$v->id."&value=false");
			echo "\n";
			flush();
			sleep(5);
			
			echo "start ".$v->id;
			echo "\n";
			flush();
			echo file_get_contents("http://localhost?l=setDeamonStatus&name=".$v->id."&value=true");
			echo "\n";
			flush();
			sleep(10);
			echo "\n";
			echo "\n";
		}	
	}
	
	
?>