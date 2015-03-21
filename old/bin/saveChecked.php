<?
error_reporting(E_ALL & ~E_NOTICE);
ini_set('display_errors',1);
include("../etc/gpio.php");


$id 	= $_REQUEST["id"];
$state 	= $_REQUEST["state"];
$gcJS = @json_decode(file_get_contents("../etc/user_gpio.conf"));



if(isset($gcJS->{$id}->active)){
	$gcJS->{$id}->active = $state;
}
else{
	@$gcJS->{$id}->active = $state;
}

file_put_contents("../etc/user_gpio.conf",json_encode($gcJS));

header("Content-Type: application/json");
echo '{status: "ok", data: "saved - '.$_GPIO['in'][$id]['name'].'"}';

?>