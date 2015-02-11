//下载应用
$(document).ready(function(e) {
    showCcHelperLayer();
});

function startupAppBox(title, download_url){
    var qrimg = document.getElementById('appbox-qr');
    qrimg.src = "http://qr.liantu.com/api.php?m=10&w=168&el=l&text=" + encodeURIComponent(download_url);
    var apptitle = document.getElementById('appbox-title');
    apptitle.innerText = title;
}

function showCcHelperLayer(){
	$(".app-download-btn-js").click(function(){
		var count = 15;
		var ccHelperLayer = $(".cc-ios-app-down-box");
		var obj = $("#close_count");
		obj.text(count);
		ccHelperLayer.zxxbox({
			title: "虫虫游戏",fix: true, bgclose:true
		});
		var startupBtn = $("#startup_cc-js");
		startupBtn.attr("href",$(this).attr("href"));
		startupBtn.click();
        startupAppBox(this.title, this.href);
		return false;
	
	});	
}