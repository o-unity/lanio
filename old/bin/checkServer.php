<?

	header("Content-Type: application/json");
	$out = intval(exec("ps -ef | grep gpioserver.py | grep -v grep | wc -l"));
	if($out > 0){
		echo '{status: "ok"}';
	}
	else{
		echo '{status: "failed"}';
	}


?>