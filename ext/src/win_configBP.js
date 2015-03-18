function includejs_<? echo $winID ?>(winID){
	
	dhxWins.window(winID).attachHTMLString('<div id="config" style="padding:20px"></div>');
	var configForm;
	configForm = new dhtmlXForm("config");
	//alert("<? echo $uri ?>");
	configForm.loadStruct("<? echo $uri ?>?l=getStaticJson&winID="+winID, function(){});	
	
	configForm.attachEvent("onChange", function(name,value,is_checked){
		alert("onChange, item name '"+name+"', value '"+value+"', is checked '"+(is_checked?"true":"false")+"'<br>");
	});
	
}

includejs_<? echo $winID ?>("<? echo $winID ?>");