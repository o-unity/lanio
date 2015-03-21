<?
error_reporting(E_ALL & ~E_NOTICE);
ini_set('display_errors',1);

	include("../etc/gpio.php");
	$gcJS = @json_decode(file_get_contents("../etc/user_gpio.conf"));
	
	$js['id'] = 0;
	
	$ct=0;
	foreach($_GPIO['in'] as $k => $v){
		$js["item"][$ct]['id'] = $k;
		$js["item"][$ct]['text'] = $v['name'];
		if(isset($gcJS->{$k}->active) AND ($gcJS->{$k}->active)){
			$js["item"][$ct]['checked'] = 1;
		}	
		$ct++;
	}
	
	echo json_encode($js);
	
	//echo "<pre>";
	//echo json_decode("{id:'0', item:[ {id:'1', text:'Port 1', child:'0' } ,{id:'2', text:'Port 2', child:'0' } ,{id:'3', text:'Port 3', child:'0' }]}");
	
?>