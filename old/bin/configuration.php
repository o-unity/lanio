<?

$name = $_REQUEST["name"];
$value = $_REQUEST["value"];

$retVal = "none";

if($name == "gpioDeamon"){
	if($value == "true"){
		
		exec("cd /var/www/lsrv/bin; sudo python gpioserver.py 2> /dev/null &",$out);
		$retVal = "gpioDeamon started...";
	}
	else{
		exec("ps -ef | grep gpioserver.py | grep -v grep | awk -F\" \" '{print $2}'",$out);
		foreach($out as $k => $v){
			exec("sudo kill $v",$out2);
		}
		$retVal = "gpioDeamon stopped...";
	}
}

header("Content-Type: application/json");
echo '{status: "ok", data: "'.$retVal.'"}';



?>