<?


$out = intval(exec("ps -ef | grep gpioserver.py | grep -v grep | wc -l"));
if($out > 0){
	$checked = "true";
}
else{
	$checked = "false";
}


echo '
[
				{type: "settings", position: "label-right", inputWidth: 42, inputHeight: 20},
				{type: "btn2state", name: "gpioDeamon", value: "1", label: "enable gpio deamon", checked: '.$checked.'},
				{type: "btn2state", name: "dhcp", value: "1", label: "dhcp server", checked: true}
];';

?>