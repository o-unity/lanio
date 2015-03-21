<?
$out = intval(exec("ps -ef | grep onewire.py | grep -v grep | wc -l"));
$i = 0;
$d[$i]['id'] = "1wireDeamon";
if($out > 0){
	$d[$i]['value'] = true;
}
else{
	$d[$i]['value'] = false;
}

$out = intval(exec("ps -ef | grep msgbus.py | grep -v grep | wc -l"));
$i++;
$d[$i]['id'] = "msgbus";
if($out > 0){
	$d[$i]['value'] = true;
}
else{
	$d[$i]['value'] = false;
}


header("Content-Type: application/json");
echo json_encode($d);
?>