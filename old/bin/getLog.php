<?

	
$md5LogFile = $_REQUEST["md5LogFile"];
$logStr = "";

	
exec('find /var/www/lsrv/log -name *.log -type f -printf \'%T@ %p\n\' | sort -n | tail -1 | cut -f2- -d" "',$outF);
$lastLogfile = $outF[0];

exec('md5sum '.$lastLogfile.' | awk -F" " \'{print $1}\'',$outM);
$md5LogFileChk = $outM[0];

if($md5LogFile != $md5LogFileChk){

	exec("tail -15 ".$lastLogfile,$out);
	foreach($out as $k => $v){
		$r = explode("INFO     -",$v);
		$out[$k] = $r[1];
	}

	$logStr = addslashes(implode("<br>",$out));
}	
	
header("Content-Type: application/json");
echo '{status: "ok", data: "'.$retVal.'", md5LogFile: "'.$md5LogFileChk.'", log: "'.$logStr.'"}';
	
?>