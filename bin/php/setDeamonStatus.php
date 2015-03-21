<?


$name = $_REQUEST["name"];
$value = $_REQUEST["value"];

$retVal = "none";

if($name == "1wireDeamon"){
	
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



header("Content-Type: application/json");
echo '{status: "ok", data: "'.$retVal.'"}';


?>