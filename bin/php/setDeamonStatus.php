<?


$name = $_REQUEST["name"];
$value = $_REQUEST["value"];

$retVal = "none";

if($name == "onewire"){
	
	$kill = "";
	exec("ps -ef | grep onewire.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
	foreach($out as $k => $v){
		$kill .= $v." ";
	}	
	
	if($value == "true"){
		if(!$kill){
			exec("cd ".$cfg->global->root."; python ./onewire.py > /dev/null 2>/dev/null &",$out);
			$retVal = "one wire deamon started...";
		}
		else{
			$retVal = "one wire deamon already started!";	
		}
	}
	else{
		exec("sudo kill ".$v,$out2);
		$retVal = "one wire deamon stopped!";
	}
}

// ------------------------------------------------------------------------


if($name == "msgbus"){
	
	$kill = "";
	exec("ps -ef | grep msgbus.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
	foreach($out as $k => $v){
		$kill .= $v." ";
	}	
	
	if($value == "true"){
		if(!$kill){
			exec("cd ".$cfg->global->root."; python ./msgbus.py > /dev/null 2>/dev/null &",$out);
			//echo "cd ".$cfg->global->root."; python ./msgbus.py > /dev/null 2>/dev/null &";
			$retVal = "message bus started...";
		}
		else{
			$retVal = "message bus already started!";	
		}
	}
	else{
		exec("sudo kill ".$v,$out2);
		$retVal = "message bus stopped!";
	}
}

// ------------------------------------------------------------------------


if($name == "display"){
	
	$kill = "";
	exec("ps -ef | grep display.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
	foreach($out as $k => $v){
		$kill .= $v." ";
	}	
	
	if($value == "true"){
		if(!$kill){
			exec("cd ".$cfg->global->root."; sudo python ./display.py > /dev/null 2>/dev/null &",$out);
			$retVal = "display listener started...";
		}
		else{
			$retVal = "display listener already started!";	
		}
	}
	else{
		exec("sudo kill -9 ".$v,$out2);
		$retVal = "display listener stopped!";
	}
}

// ------------------------------------------------------------------------


if($name == "gpi"){
	
	$kill = "";
	exec("ps -ef | grep gpi.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
	foreach($out as $k => $v){
		$kill .= $v." ";
	}	
	
	if($value == "true"){
		if(!$kill){
			exec("cd ".$cfg->global->root."; sudo python ./gpi.py > /dev/null 2>/dev/null &",$out);
			$retVal = "gpi deamon started...";
		}
		else{
			$retVal = "gpi deamon already started!";	
		}
	}
	else{
		exec("sudo kill ".$v,$out2);
		$retVal = "gpi deamon stopped!";
	}
}

// ------------------------------------------------------------------------


if($name == "gpo"){
	
	$kill = "";
	exec("ps -ef | grep gpo.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
	foreach($out as $k => $v){
		$kill .= $v." ";
	}	
	
	if($value == "true"){
		if(!$kill){
			exec("cd ".$cfg->global->root."; sudo python ./gpo.py > /dev/null 2>/dev/null &",$out);
			$retVal = "gpi listner started...";
		}
		else{
			$retVal = "gpi listner already started!";	
		}
	}
	else{
		exec("sudo kill ".$v,$out2);
		$retVal = "gpi listner stopped!";
	}
}



header("Content-Type: application/json");
echo '{status: "ok", data: "'.$retVal.'"}';


?>