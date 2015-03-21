
function includejs_<? echo $winID ?>(winID){
	
	dhxWins.window(winID).attachHTMLString('<div id="config" style="padding:20px"></div>');
	var configForm;
	configForm = new dhtmlXForm("config");
	//alert("<? echo $uri ?>");
	configForm.loadStruct("<? echo $uri ?>?l=getStaticJson&winID="+winID, function(){
		getDeamonStatus(configForm,winID);
	});	
	
	configForm.attachEvent("onChange", function(name,value,is_checked){
		//alert("?l=setDeamonStatus&name="+name+"&value="+(is_checked?"true":"false"))
		window.dhx4.ajax.put("?l=setDeamonStatus&name="+name+"&value="+(is_checked?"true":"false"), "", function(r){
			var t = window.dhx4.s2j(r.xmlDoc.responseText);
			dhtmlx.message({
				type: "info",
				text: t.data
			});
		});	
	});
	
}


function getDeamonStatus(cf,winID) {
	
	if (window.winRegId) {
		if (!window.winRegId[winID]) {
			return true;	
		}
	}
	
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
		
		chkSrv = setTimeout( function() { getDeamonStatus(cf,winID); } , 5000);
	});
}

includejs_<? echo $winID ?>("<? echo $winID ?>");