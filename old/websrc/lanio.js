		var myLayout, myMenu, myToolbar, myRibbon, sbObj;
		function doOnLoad() {
			
			myLayout = new dhtmlXLayoutObject({
				parent: document.body,
				pattern: "3J"
			});
			
			myLayout.cells("a").setWidth(300);
			myLayout.cells("a").setText("ports");
			myLayout.cells("b").setText("configuration");
			myLayout.cells("c").setText("debug");
			
			myLayout.cells("b").attachObject("configuration");
			
			attachStatusBar();
			//attachHeader();
			myLayout.attachHeader("my_logo");
			checkHeight();
			
			
			myLayout.cells("a").hideHeader();
			myAcc = myLayout.cells("a").attachAccordion({
				icons_path: "../common/icons/",
				items: [
					{ id: "a1", text: "Inputs" },
					{ id: "a2", text: "Relays" },
					{ id: "a3", text: "Configuration" }
				]
			});
			
			
			tree=new dhtmlXTreeObject("treeboxbox_tree","100%","100%",0);
			tree.setImagePath("dhtmlx/skins/terrace/imgs/dhxtree_terrace/");
			tree.enableCheckBoxes(1);
			tree.setXMLAutoLoading("bin/gpiotree.php"); 
			tree.setDataMode("json");
			//load first level of tree
			tree.loadJSON("bin/gpiotree.php?id=0"); 
			tree.setOnClickHandler(tonclick);
			tree.setOnCheckHandler(toncheck);
			myAcc.cells("a1").attachObject("treeboxbox_tree");
			myAcc.cells("a3").attachObject("config");
			//myAcc.cells("c").attachObject("debug");
			
			var configForm;
			configForm = new dhtmlXForm("config");
			configForm.loadStruct("bin/getConfig.php", function(){});	
			configForm.attachEvent("onChange", function(name,value,is_checked){
				//alert("onChange, item name '"+name+"', value '"+value+"', is checked '"+(is_checked?"true":"false")+"'<br>");
				window.dhx4.ajax.put("bin/configuration.php?name="+name+"&value="+(is_checked?"true":"false"), "", function(r){
					setCheckServer();
					var t = window.dhx4.s2j(r.xmlDoc.responseText);
				    sbObj.setText(t.data);
				});		
		
		
			});
			
			checkServer();
			setCheckServer();
			
		}
		
		function doOnClick(e){
			e = e||event;
			var t = (e.target||e.srcElement);
			alert("custom onclick event: "+t._idd+"<br>");
		}
		
		
		
		function loadXForm(id){
			
			myLayout.cells("b").attachHTMLString('<div id="configuration" style="padding:20px"><div id="myForm"></div></div>');
			
			var myForm, formData;
			myForm = new dhtmlXForm("myForm");
			
			myForm.loadStruct("bin/getForm.php?id="+id, function(){});
			myForm.attachEvent("onButtonClick", function(name){
				//alert("onButtonClick event called, item name '"+name+"' ");

				myForm.send("bin/savePortConfig.php", function(loader, r){
					setCheckServer();
					var t = window.dhx4.s2j(r);
			    	sbObj.setText(t.data);
				});

			});
		}
		
		// header
		function attachHeader() {
			document.getElementById("my_logo").style.display = "";
			myLayout.attachHeader("my_logo");
			checkHeight();
		}
		// status bar
		function attachStatusBar() {
			if (sbObj != null) return;
			sbObj = myLayout.attachStatusBar();
			checkHeight();
		}
		// fix cells' height
		function checkHeight() {
			myLayout.cells("b").setHeight(Math.round(myLayout.cells("a").getHeight()/3));
		}
		function tonclick(id){
			loadXForm(id);
		 };
		function toncheck(id,state){
			window.dhx4.ajax.put("bin/saveChecked.php?id="+id+"&state="+state, "", function(r){
			    setCheckServer();				
				var t = window.dhx4.s2j(r.xmlDoc.responseText);
			    sbObj.setText(t.data);
			});
		};	


if (typeof(md5LogFile) !== 'undefined') {
	var md5LogFile = "";
}


function setCheckServer() {
	if (typeof(chkSrv) !== 'undefined') {
		window.clearInterval(chkSrv);
	}
    chkSrv = setInterval(checkServer, 2000);
}
		
function checkServer() {
	window.dhx4.ajax.put("bin/checkServer.php", "", function(r){
		var t = window.dhx4.s2j(r.xmlDoc.responseText);
		if(t.status == "ok"){
			sbObj.setText("<img src='dhtmlx/samples/dhtmlxForm/common/button2state/toggle_on.png' style='float: left;height: 15px;padding-right:5px' /> gpio deamon");	
		}
		else{
			sbObj.setText("<img src='dhtmlx/samples/dhtmlxForm/common/button2state/toggle_off.png' style='float: left;height: 15px;padding-right:5px' /> gpio deamon");	
		}
	    
	});
	
	window.dhx4.ajax.put("bin/getLog.php?md5LogFile="+md5LogFile, "", function(r){
		var t = window.dhx4.s2j(r.xmlDoc.responseText);
		if(t.md5LogFile != md5LogFile){
			myLayout.cells("c").attachHTMLString('<pre style="font-size:9px">'+t.log+'</pre>');
		}
		md5LogFile = t.md5LogFile;
	});
	
}		