
var ccplayButtonState = function(installSelector,downloadBtnSelector) {
	
	this.downloadBtnTxt = ["立即下载","暂停下载","继续下载","已下载"];
	this.installBtnTxt = ["立即安装","立即升级","已经安装"];
	this.UNDOWNLOAD = "10000";
	this.DOWNLOADING = "2";
	this.PAUSE = "50";
	this.COMPLETED = "100";
	this.INSTALLED_NORMAL = "INSTALLED_NORMAL";
	this.CAN_UPDATE = "CAN_UPDATE";
	this.NO_INSTALLED = "NO_INSTALLED";
	
	this.downloadAppInfos = {};
	this.nativeAppInfos = {};
	this.deviceList = {};
	this.deviceUid = [];
	this.installBtns = $(installSelector);
	this.downloadBtns = $(downloadBtnSelector);
	this.init();
};

ccplayButtonState.prototype = {
	
	init:function(){
		this.installBtns.attr("state",this.UNDOWNLOAD);
		this.downloadBtns.attr("state",this.UNDOWNLOAD);
		this.downloadBtns.text(this.downloadBtnTxt[0]);
		this.installBtns.text(this.installBtnTxt[0]);
		this.bindDownloadBtnEv();
		this.bindInstallBtnEv();
		this.getDownloadInfo();
		this.getDeviceListInfo();
	},
	
	/**
	 * 绑定下载按钮的事件
	 * @return void
	 * @author zhangbp
	 */
	
	bindDownloadBtnEv:function(){
		_this = this;
		this.downloadBtns.bind('click',function(){
			var _thisBtn = $(this);
			var download_state = _thisBtn.attr("state");
			var dataJson = eval("(" + _thisBtn.parent().attr("data-json") + ")");
			switch (download_state) {
			 	case _this.DOWNLOADING:
				 	window.external.PauseDownload(dataJson.download_url);
				 	_thisBtn.attr("state",_this.PAUSE);
			 	break;
			 	case _this.PAUSE:
			 		window.external.ResumeDownload(dataJson.download_url);
			 		_thisBtn.attr("state",_this.DOWNLOADING);
			 	break;
			 	case _this.UNDOWNLOAD:
			 		window.external.BeginShareDownload2(dataJson.download_url,dataJson.title, dataJson.package_name, dataJson.appid);
			 		_thisBtn.attr("state",_this.DOWNLOADING);
			 	break;
			}
			_this.updateDownloadBtnItemState(_thisBtn);
		});
		
	},
	
	/**
	 * 更新下载按钮的状态,单一的btn
	 * @param downloadBtn 下载按钮
	 * @return void
	 * @author zhangbp
	 */
	
	updateDownloadBtnItemState:function(downloadBtn){
		
		var download_state = downloadBtn.attr("state");
		if(download_state != undefined){
			switch (download_state.toString()) {
			 	case this.DOWNLOADING:
			 		downloadBtn.text(this.downloadBtnTxt[1]);
			 	break;
			 	case this.PAUSE:
			 		downloadBtn.text(this.downloadBtnTxt[2]);
			 	break;
			 	case this.COMPLETED:
			 		downloadBtn.text(this.downloadBtnTxt[3]);
			 	break;
			 	default:
			 		downloadBtn.text(this.downloadBtnTxt[0]);
			 	break;
		  }
		}
	},
	
	/**
	 * 更新下载按钮的状态，从下载信息downloadAppInfos里更新
	 * @param downloadBtn 下载按钮
	 * @return void
	 * @author zhangbp
	 */
	
	updateDownloadBtnState:function(){
		
		for(var i = 0;i < this.downloadBtns.size();i++){
			var downloadBtn = this.downloadBtns.eq(i);
			var dataJson = eval("(" + downloadBtn.parent().attr("data-json") + ")");
			var download_state = this.downloadAppInfos[dataJson.download_url];
			if(download_state != undefined){
				var download_state_str = download_state.toString();
				if(download_state_str != this.DOWNLOADING && download_state_str != this.PAUSE && download_state_str != this.COMPLETED){
					download_state = this.UNDOWNLOAD;
				}
				downloadBtn.attr("state",download_state);
			}else{
				downloadBtn.attr("state",this.UNDOWNLOAD);
			}
			this.updateDownloadBtnItemState(downloadBtn);
		}
	},
	
	/**
	 * 绑定安装按钮的事件
	 * @return void
	 * @author zhangbp
	 */
	
	bindInstallBtnEv:function(){
		_this = this;
		this.installBtns.bind('click',function(){
			var _thisBtn = $(this);
			var install_state = _thisBtn.attr("state");
				
			var dataJson = eval("(" + _thisBtn.parent().attr("data-json") + ")");
			if(install_state == _this.NO_INSTALLED || install_state == _this.CAN_UPDATE){
				if(_this.deviceUid.length > 1){
					_this.createDeviceList();
					var popDiv = $("#install-popup-js");
					popDiv.css({"left":""+_thisBtn.offset().left+"px","top":""+_thisBtn.offset().top+"px"}).show();
					$("#install-popup-js > a").bind('click',function(){
						var uuid = $(this).attr("deviceKey");
						window.external.InstallShareApp2(dataJson.download_url, dataJson.title,uuid, dataJson.package_name , dataJson.appid, 0);
						popDiv.hide();
					});
				}else{
					window.external.InstallShareApp2(dataJson.download_url, dataJson.title,_this.deviceUid[0], dataJson.package_name , dataJson.appid, 0);
				}
			}
			
		});
		
	},
	
	/**
	 * 更新安装按钮的状态,单一的btn
	 * @param installBtn 安装按钮
	 * @return void
	 * @author zhangbp
	 */
	
	updateInstallBtnItemState:function(installBtn){
		
		var install_state = installBtn.attr("state");
		if(install_state != undefined){
			switch (install_state.toString()) {
			 	
			 	case this.NO_INSTALLED:
			 		installBtn.text(this.installBtnTxt[0]);
			 	break;
			 	case this.INSTALLED_NORMAL:
			 		installBtn.text(this.installBtnTxt[2]);
			 	break;
			 	case this.CAN_UPDATE:
			 		installBtn.text(this.installBtnTxt[1]);
			 	break;
		  }
		}
	},
	
	
	/**
	 * 更新安装按钮的状态
	 * @param downloadBtn 安装按钮
	 * @return void
	 * @author zhangbp
	 */
	
	updateInstallBtnState:function(){
		
		if($.isEmptyObject(this.deviceList)){
			this.installBtns.attr("disabled",true);
			this.installBtns.text(this.installBtnTxt[0]);
			this.installBtns.toggleClass("no",true);
		}else{
			
			for(var i = 0;i < this.installBtns.size();i++){
				var installBtn = this.installBtns.eq(i);
				var dataJson = eval("(" + installBtn.parent().attr("data-json") + ")");
				
				var nativeitemApp = this.nativeAppInfos[dataJson.download_url];
				if(nativeitemApp != undefined){
					if(nativeitemApp[1] < dataJson.version_name){
						installBtn.attr("state",this.CAN_UPDATE);
					}else{
						installBtn.attr("state",this.INSTALLED_NORMAL);
					}
				}else{
					installBtn.attr("state",this.NO_INSTALLED);
				}
				
				if(installBtn.attr("state") == this.INSTALLED_NORMAL || this.downloadAppInfos[dataJson.download_url] != undefined){
					installBtn.toggleClass("no",true);
					installBtn.attr("disabled",true);
				}else{
					installBtn.toggleClass("no",false);
					installBtn.attr("disabled",false);
				}
				
				this.updateInstallBtnItemState(installBtn);
			}
		}
		
	},
	
	/**
	 * 下载信息
	 * @return void
	 * @author zhangbp
	 */
	getDownloadInfo:function(){
		var info = window.external.GetDownloadInfo(-1);
		if(info != null){
			var result = eval("(" + info + ")").result
			this.downloadAppInfos = {};
			for(app in result){
				this.downloadAppInfos[result[app][0]] = result[app][1];
			}
		}
		
		this.updateDownloadBtnState();
	},
	
	/**
	 * 设备信息
	 * @return void
	 * @author zhangbp
	 */
	getDeviceListInfo:function(){
		var _this = this;
		setInterval(function() {
				var data = window.external.GetDeviceListInfo();
				_this.deviceList = eval("(" + data + ")");
				_this.deviceUid = [];
				var ii = -1;
				for(var list in _this.deviceList){
					var deviceItem = _this.deviceList[list];
					for(var i = 0;i < deviceItem.app.length;i++){
						_this.nativeAppInfos[deviceItem.app[i][0]] = deviceItem.app[i];
					}
					_this.deviceUid[++ii] = list;
				}
				_this.updateInstallBtnState();
			},
		500);
	},
	
	/**
	 * 创建设备列表
	 * @return void
	 * @author zhangbp
	 */
	
	createDeviceList:function(){
		var html = "<span>选择安装设备</span>";
		for(var list in this.deviceList){
			var deviceItem = this.deviceList[list];
			html += "<a href=\"javascript:;\" deviceKey = \""+list+"\" ><i>√</i>"+deviceItem.name+"</a>";
		}
			
		if($("#install-popup-js").size() == 0){
			$("body").append("<div class=\"install-popup\" id=\"install-popup-js\"></div>");
		}
		$("#install-popup-js").html(html);
		$("#install-popup-js").hover(function(){
			$(this).show();
		},function(){
			$(this).hide();
		});
	}
};

function downloadStateChanged(c, d, a) {
	
	if(mccplayButtonState != undefined){
		mccplayButtonState.getDownloadInfo();
	}
}

$(document).ready(function(){
	mccplayButtonState = new ccplayButtonState(".app-install-btn-js",".app-download-btn-js");

});

