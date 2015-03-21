<?
error_reporting(E_ALL & ~E_NOTICE);
ini_set('display_errors',1);

$id 	= $_REQUEST["id"];
$gcJS = @json_decode(file_get_contents("../etc/user_gpio.conf"));
include("../etc/gpio.php");

$js = '[
	{type: "settings", position: "label-left", labelWidth: 130, inputWidth: 220},
	{type: "fieldset", label: "'.$_GPIO['in'][$id]['name'].' configuration", inputWidth: 440, list:[
		{type: "hidden", name:"id", value:"'.$id.'"},
		{type: "select", label: "Event Type",  name: "ETYPE", options:[
			{text: "Falling Edge", value: "FE"'.(@$gcJS->{$id}->ETYPE == "FE" ? ", selected: true" : "").'},
			{text: "Rising Edge", value: "RE"'.(@$gcJS->{$id}->ETYPE == "RE" ? ", selected: true" : "").'},
			{text: "Both", value: "BOTH"'.(@$gcJS->{$id}->ETYPE == "BOTH" ? ", selected: true" : "").'}
		]},
		{type: "input", label: "Event URL", value: "'.@addslashes($gcJS->{$id}->EURL).'", name: "EURL"},
		{type: "select", label: "Request Type", name: "REQUESTTYPE", options:[
			{text: "POST", value: "POST"'.(@$gcJS->{$id}->REQUESTTYPE == "POST" ? ", selected: true" : "").'},
			{text: "GET", value: "GET"'.(@$gcJS->{$id}->REQUESTTYPE == "GET" ? ", selected: true" : "").'}
		]},
		{type: "input", label: "Data", value: "'.@addslashes($gcJS->{$id}->DATA).'", name: "DATA", note: {
					text: "you can integrate  ##value## to submit the current value"
				}},
		{type: "input", label: "Content Type", value: "'.@addslashes($gcJS->{$id}->CONTENTTYPE).'", name: "CONTENTTYPE"},
		{type: "checkbox", name: "type", label: "Authentification", labelWidth: "auto", position: "label-right", name: "AUTH"'.(@$gcJS->{$id}->AUTH == "1" ? ", checked: true" : "").', list:[
			{type: "input", label: "user name", value: "'.@addslashes($gcJS->{$id}->USR).'", name: "USR"},
			{type: "input", label: "password", value: "'.@addslashes($gcJS->{$id}->PASS).'", name: "PASS"}
		]},
		{type: "newcolumn"},
		{type: "button", value: "Save", name: "button_submit"}
	]}
]';

header("Content-Type: application/json");
echo $js;

?>