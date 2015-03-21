<?
	echo "<pre>";
	
	
	//md5sum 20150217_gpioserver.log | awk -F" " '{print $1}'
	exec('find /var/www/lsrv/log -name *.log -type f -printf \'%T@ %p\n\' | sort -n | tail -1 | cut -f2- -d" "',$outF);

	exec("tail -15 ".$outF[0],$out);
	foreach($out as $k => $v){
		echo $v."\n";
	}
	

	//sudo python gpioserver.py
	echo "done";
?>