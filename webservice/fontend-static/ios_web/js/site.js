//下载应用
$(document).ready(function(e) {
    showCcHelperLayer();
});

function startupCchelper(url){
	var url = "cchelper://"+url;
	var j = document.getElementById('tbapijumb');
	if(j==null){
		j = document.createElement('iframe');
		j.style.display = "none";
		j.id = 'tbapijumb';
		document.body.appendChild(j);
	}
	j.src = url;
}

function showCcHelperLayer(){
	var ii;			
	$(".app-download-btn-js").click(function(){
		var count = 15;
		var ccHelperLayer = $(".cc-ios-app-down-box");
		var obj = $("#close_count");
		obj.text(count);
		ccHelperLayer.zxxbox({
			title: "虫虫游戏",fix: true, bgclose:true
		});
		if(ii != undefined){
			clearInterval(ii);
		}
		ii = setInterval(function(){
			count--;
			obj.text(count);
			if(count == 0){
				//$.zxxbox.hide();
				clearInterval(ii);
			}
		},1000);
		var startupBtn = $("#startup_cc-js");
		startupBtn.attr("href",$(this).attr("href"));
		startupBtn.click();
		return false;
	
	});	
	$("#startup_cc-js").click(function(){
			startupCchelper($(this).attr("href"));
			return false;
	});
}