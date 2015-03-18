var myLayout, myMenu, myToolbar, myRibbon, sbObj;

function doOnLoad() {


	myLayout = new dhtmlXLayoutObject({
		parent: document.body,
		pattern: "2U"
	});

	myLayout.cells("a").setWidth(300);
	myLayout.cells("a").setText("ports");

	//myLayout.cells("b").attachObject("workspace");

	myLayout.cells("a").setText("");
	myLayout.cells("b").setText("ebrixx configurator");

	attachStatusBar();

	myToolbarJSON = new dhtmlXToolbarObject({
		parent: "toolbarObj",
		icons_path: "ext/img/",
		json: "etc/staticjson/headB_menu.json",
		onload: function() {}
	});
	myLayout.cells("b").attachObject("toolbarObj");
	document.getElementById("winVP").setAttribute("style", "height:" + (Math.round(myLayout.cells("b").getHeight()) - 80) + "px;");


	// ---------------------------------------------
	// GET ACTIVE WINDOWS
	window.dhx4.ajax.get("?l=winGetActive", function(r) {
		var t = JSON.parse(r.xmlDoc.responseText);
		if (t !== null) {
			t.forEach(function(item) {
				openWin(item.buttonId);
			});
		}
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
		if (sbObj !== null) return;
		sbObj = myLayout.attachStatusBar();
		checkHeight();
	}
	// fix cells' height
function checkHeight() {
	myLayout.cells("b").setHeight(Math.round(myLayout.cells("a").getHeight() / 3));
}



function openWin(obj) {
	myLayout.cells("b").progressOn();
	window.dhx4.ajax.get("?l=winStruct&obj=" + obj, function(r) {
		var t = JSON.parse(r.xmlDoc.responseText);

		// CHECK IF ALREADY OPPEN
		if (window.winRegId) {
			if (window.winRegId[t.id]) {
				dhtmlx.message({
					type: "info",
					text: "window already open"
				});
				myLayout.cells("b").progressOff();
				return true;
			}
		}

		// MARK FOR FURTHER PROZESSING
		window.winRegId = [t.id];
		window.winRegId[t.id] = true;

		// CREATE WINDOW, BASED ON JSON
		dhxWins = new dhtmlXWindows({
			viewport: {
				object: "winVP"
			},
			wins: [t],
		});

		// CREATE EVENTS
		dhxWins.attachEvent("onMoveFinish", function(win) {
			saveWinPosition(win, true);
		});

		dhxWins.attachEvent("onResizeFinish", function(win) {
			saveWinPosition(win, true);
		});

		dhxWins.attachEvent("onClose", function(win) {
			saveWinPosition(win, false);
			window.winRegId[win.getId()] = false;
			return true;
		});

		// UPDATE WINDOW NAME
		dhxWins.window(t.id).setText(myToolbarJSON.getItemText(t.buttonId));

		// APPEND AND PROGRESS OFF
		myLayout.cells("b").appendObject("winVP");
		myLayout.cells("b").progressOff();
		
		// LOAD NOW CONTENT TO WINDOW
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = "?l=winLoadJS&winID="+t.id;
		document.body.appendChild(script);         

		// SAVE POSITION
		saveWinPosition(dhxWins.window(t.id),true);
		
	});
}

function saveWinPosition(win, active) {
	window.dhx4.ajax.get("?l=winAttSave&obj=" + win.getId() +
		"&position=" + win.getPosition() + "&maxHeight=" +
		myLayout.cells("b").getHeight() + "&maxWidth=" +
		myLayout.cells("b").getWidth() + "&dimension=" +
		win.getDimension() + "&active=" + active,
		function(r) {
			var t = window.dhx4.s2j(r.xmlDoc.responseText);
			if (t === null) {
				dhtmlx.message({
					type: "error",
					text: "upps, could not save position<br><br>" + r.xmlDoc.responseText
				});
			}

		});
}