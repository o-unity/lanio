
function includejs_<? echo $winID ?>(winID){
	
	dhxWins.window(winID).attachHTMLString('<div id="config" style="padding:20px"></div>');
	var configForm;
	configForm = new dhtmlXForm("config");
	//alert("<? echo $uri ?>");
	configForm.loadStruct("<? echo $uri ?>?l=getStaticJson&winID="+winID, function(){
		getDeamonStatus(configForm);
	});	
	
	configForm.attachEvent("onChange", function(name,value,is_checked){
		//alert("onChange, item name '"+name+"', value '"+value+"', is checked '"+(is_checked?"true":"false")+"'<br>");
	});
	
}


function getDeamonStatus(cf) {
	//alert(winID); 
	window.dhx4.ajax.put("?l=getDeamonStatus", "", function(r){
		var t = window.dhx4.s2j(r.xmlDoc.responseText);
		
		if (t !== null) {
			t.forEach(function(item) {
				if(item.value === true){
					cf.checkItem(item.id);	
				}
				else{
					cf.uncheckItem(item.id);	
				}
			});
		}
		
		chkSrv = setTimeout( function() { getDeamonStatus(cf); } , 5000);
	});
}

includejs_<? echo $winID ?>("<? echo $winID ?>");