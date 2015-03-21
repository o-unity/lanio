<?

//print_r($_REQUEST);
include("../etc/gpio.php");
$gcJS = @json_decode(file_get_contents("../etc/user_gpio.conf")); 

$id = $_REQUEST["id"];
@$gcJS->{$id}->ETYPE 		= $_REQUEST["ETYPE"];
@$gcJS->{$id}->EURL 		= $_REQUEST["EURL"];
@$gcJS->{$id}->REQUESTTYPE 	= $_REQUEST["REQUESTTYPE"];
@$gcJS->{$id}->DATA 		= $_REQUEST["DATA"];
@$gcJS->{$id}->AUTH 		= $_REQUEST["AUTH"];
@$gcJS->{$id}->USR 			= $_REQUEST["USR"];
@$gcJS->{$id}->PASS 		= $_REQUEST["PASS"];
@$gcJS->{$id}->CONTENTTYPE 	= $_REQUEST["CONTENTTYPE"];


file_put_contents("../etc/user_gpio.conf",json_encode($gcJS));
header("Content-Type: application/json");
echo '{status: "ok", data: "saved - '.$_GPIO['in'][$id]['name'].'"}';

/*
Array
(
	[id] => 17
    [ETYPE] => RE
    [EURL] => URL
    [PORT] => PORT
    [REQUESTTYPE] => 
    [DATA] => DATA
    [AUTH] => 1
    [USR] => usr
    [PASS] => pass
    [4608ee4b961f37eecb8c9e7dbe2ce51e] => rmtu6p05g9jeeti0mig83hlbj1
)

*/



?>