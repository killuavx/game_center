cc_pc_ios = {}; 
cc_body = $("body");
(function(a){

	a.init = function(b, c)
	{
	
		a.setupBtn = $(b);
		a.downBtn = $(c);
		a.initDownBtn();
		a.downBtnUpdate();
		a.getDeviceJsonInfo();
	};	
})(cc_pc_ios);

(function(a){	
	a.getDeviceJsonInfo = function()
	{
		a.deviceList = {};
		a.uuid = [];
		setTimeout(function()
			{
				a.deviceList = eval("(" + external.GetDeviceListInfo().replace(/[\n|\r]/gm, "") + ")");
				a.uuid = [];
	            for (var dev in a.deviceList) 
	            {
	            	a.uuid.push(dev);
	            }
				a.updateSetupBtn();
			}, 100);
	};

	a.updateSetupBtn = function ()
	{		
		var deviceNum = a.uuid.length;
		$(".install-popup").remove();
		if(deviceNum == 0)
		{
			a.setupBtn.attr("disabled",true);
			a.setupBtn.text("无设备");
			a.setupBtn.attr("title", "未检测到设备");
			a.setupBtn.toggleClass("no",true);
			a.setupBtn.attr("state", 0);
		}else if(deviceNum == 1)
		{
			
			a.updateOneDeviceSetupBtn();
			
		}else if(deviceNum > 1)
		{
		
			a.updateMoreOneDeviceSetupBtn(deviceNum);
		}
		
	};

	
	a.updateOneDeviceSetupBtn = function()
	{
	
			 for (var i = 0; i < a.setupBtn.length; i++) 
			 {				
				 var setup_Btn = a.setupBtn.eq(i);					 
				 var appInfo = eval("(" + setup_Btn.parent().attr("data-json") + ")");			 
                 var sCompareResult = compareSoft(a.uuid[0], appInfo.package_name, appInfo.version_name);              
				 
				if(sCompareResult != 5)
                {
					setup_Btn.attr("state", 0);
					setup_Btn.attr("title", "安装应用到：" + a.deviceList[a.uuid[0]].name); 
					a.setupBtn.attr("disabled",false);
					a.setupBtn.toggleClass("no",false);
				}
				
				if(sCompareResult == 1 || sCompareResult == 4)
				{
					setup_Btn.text("立即安装");
					
				}else if(sCompareResult = 2)
				{
					setup_Btn.text("已经安装");
					
				}else if(sCompareResult == 3)
				{
					setup_Btn.text("立即升级");
					
				}
				
               setup_Btn.bind('click',function(ii, cr) 
                	{
						return function()
						{		
							if($(this).attr("state") == 1)
							{
								return;
							}
							
							var nOption = 0;
							 if (cr == 1 || cr == 2 || cr == 4) 
							 { 
								 $(this).attr("title", "后台正在为设备[" + a.deviceList[a.uuid[0]].name + "]安装该应用程序");
								 nOption = 0
							 } else 
							 {
								 if (cr == 3) 
								 {
									 $(this).attr("title", "后台正在为设备[" + a.deviceList[a.uuid[0]].name + "]升级该应用程序");
									 nOption = 1
								 }
							 }
							 try {
								 external.InstallShareApp2(ii.download_url, ii.title + ".ipa", a.uuid[0], ii.package_name , ii.appid, nOption);
							 } catch(error) {}
							 $(this).attr("state", 1);
							 $(this).attr("disabled", true);
							 $(this).text("安装中");
					         $(this).toggleClass("no", true);
						
						}
                     }(appInfo, sCompareResult));
             }
	};
	
	a.updateMoreOneDeviceSetupBtn = function(devNum)
	{
			for (var i = 0; i < a.setupBtn.length; i++)
			{
				var setup_Btn = a.setupBtn.eq(i);
			    var appInfo = eval("(" + setup_Btn.parent().attr("data-json") + ")");
			
                var cr1 = cr2 = cr3 = 0;
                var $objDcSelect = $('<div class="install-popup" style= "display:none"><span>请选择以下设备</span></div>');
				
                for (var j = 0; j < a.uuid.length; j++) 
				{
                    var  sCompareResult =  compareSoft(a.uuid[j], appInfo.package_name, appInfo.version_name);
                    
                    if( sCompareResult != 5)
                    {
                    	setup_Btn.attr("state", 0);
						setup_Btn.attr("title", "选择安装应用的设备"); 
						a.setupBtn.attr("disabled",false);
						a.setupBtn.toggleClass("no",false);;
                    }
                    
                    var objDc = document.createElement("a");
					//objDc.href = 'javascript:void(0)';
                    objDc.innerHTML = a.deviceList[a.uuid[j]].name;  
                    objDc.title = "安装应用到：" + a.deviceList[a.uuid[j]].name;
				
                    if (sCompareResult == 1 || sCompareResult == 4) 
					{
                        cr1 += 1;
						
                        objDc.onclick = (function(ii, jj, tempBtn)
						{
                            return function() 
							{
								$(this).parent().css("display", "none");
                                try { 
                                    external.InstallShareApp2(ii.download_url, ii.title + ".ipa", a.uuid[jj], ii.package_name , ii.appid, 0);
                                } catch(error) {}
                                tempBtn.attr("title", "后台正在为设备[" + a.deviceList[a.uuid[jj]].name + "]安装该应用程序");
								tempBtn.attr("state", 1);
								tempBtn.attr("disabled", true);
								tempBtn.text("安装中");
								tempBtn.toggleClass("no", true);
                            }
                        })(appInfo, j, setup_Btn);
						
                    } else 
					{
                        if (sCompareResult == 2) 
						{
                            cr2 += 1;
                            objDc.title = "重新安装应用到：" + a.deviceList[a.uuid[j]].name;
                            objDc.onclick = (function(ii, jj, tempBtn) 
							{
                                return function() 
								{   
									$(this).parent().css("display", "none");
                                    try {
                                        
                                        external.InstallShareApp2(ii.download_url, ii.title + ".ipa", a.uuid[jj], ii.package_name , ii.appid, 0);
                                    } catch(error) {}
                                    tempBtn.attr("title", "后台正在为设备[" + a.deviceList[a.uuid[jj]].name + "]重新安装该应用程序");
									tempBtn.attr("state", 1);
									tempBtn.attr("disabled", true);
									tempBtn.text("安装中");
									tempBtn.toggleClass("no", true);
                                }
                            })(appInfo, j, setup_Btn);
							
                        } else 
						{
                            if (sCompareResult == 3) 
							{
                                cr3 += 1;
								objDc.title = "升级安装应用到：" + a.deviceList[a.uuid[j]].name;
                                objDc.onclick = (function(ii, jj, tempBtn) 
								{
                                    return function() {
										$(this).parent().css("display", "none");
                                        try {
                                           
                                            external.InstallShareApp2(ii.download_url, ii.title + ".ipa", a.uuid[jj], ii.package_name , ii.appid, 1);
                                        } catch(error) {}
                                       
                                        tempBtn.attr("title", "后台正在为设备[" + a.deviceList[a.uuid[jj]].name + "]升级该应用程序");
										tempBtn.attr("state", 1);
										tempBtn.attr("disabled", true);
										tempBtn.text("安装中");
										tempBtn.toggleClass("no", true);    
                                    }
                                })(appInfo, j, setup_Btn);
                            }
                        }
                    }
					
                    $objDcSelect[0].appendChild(objDc);	
					
                }
				
				$objDcSelect.unbind("hover").hover(function() {},
                    function() 
					{
                        $(this).fadeOut(150)
                    });
                setup_Btn.$objDcSelect = $objDcSelect
				
				
				cc_body.append($objDcSelect[0]);
				
				setup_Btn.text("立即安装");
				
                if (cr1 == a.uuid.length) 
				{ 
					setup_Btn.text("立即安装");
                }else if (cr2 == a.uuid.length) 
				{
                    
					setup_Btn.text("重新安装");
                }else if (cr3 == a.uuid.length) 
				{
               
					setup_Btn.text("立即更新");
                }
                setup_Btn.unbind("click").bind("click", function(ii) 
				{
                    return function() 
					{
						if(ii.attr("state") == 1)
						{
								return;
						}
						var x = ii.offset().left;
						var y = ii.offset().top - 10;
						ii.$objDcSelect.css({"left":"" + x + "px", "top":"" + y + "px"});
                        ii.$objDcSelect.fadeIn(200)
                    }
                }(setup_Btn));
			}
	};
	
	function compareVer(sDeviceSoftVer, sPcSoftVer) 
	{
	    if (!sDeviceSoftVer || !sPcSoftVer) 
		{
	        return 0
	    }
	    var i, j, n;
	    sDeviceSoftVer = (sDeviceSoftVer + "").split(".");
	    sPcSoftVer = (sPcSoftVer + "").split(".");
	    j = sDeviceSoftVer.length >= sPcSoftVer.length ? sDeviceSoftVer.length: sPcSoftVer.length;
	    for (i = 0; i < j; i++) 
		{
	        if (!sDeviceSoftVer[i]) 
			{
	            sDeviceSoftVer[i] = 0
	        }
	        if (!sPcSoftVer[i]) 
			{
	            sPcSoftVer[i] = 0
	        }
	        if (parseInt(sDeviceSoftVer[i]) == parseInt(sPcSoftVer[i])) 
			{
	            n = 1
	        } else 
			{
	            if (parseInt(sDeviceSoftVer[i]) > parseInt(sPcSoftVer[i])) 
				{
	                n = 1;
	                i = j
	            } else {
	                n = 2;
	                i = j
	            }
	        }
	    }
	    return n
	};
	
	function compareSoft(uuid, bundleId, pcSoftVer) {
	    if (!uuid || !a.deviceList[uuid] || !bundleId || !pcSoftVer)
		{
	        return 0
	    }
	    var deviceApp, i, j, n = 1;
	    deviceApp = a.deviceList[uuid].app;
	    for (i = 0; i < deviceApp.length; i++) 
		{
	        if (deviceApp[i][0] == bundleId) 
			{
	            n = 2;				
	            if (deviceApp[i][2] == 4) 
				{
	                n = 4
	                
	            }else if(deviceApp[i][2] == 2 || deviceApp[i][2] == 3)
	            {
	            	n = 5;
	            	
	            }else if (compareVer(deviceApp[i][1], pcSoftVer) == 2) 
				{
	                n = 3 
	            }
	            break;
	        }
	    }
	    return n
	}
	
})(cc_pc_ios);


(function(a){	
	a.initDownBtn = function()
	{
		a.downState = {error: ["重新下载", "下载失败，点击重试", -1], begin: ["立即下载", "下载到本地", 0],  downloading: ["正在下载", "正在下载中，点击暂停", 2],  pause: ["暂停下载", "点击继续下载", 50], ok: ["已经下载", "点击可重新下载", 100]};
		a.downBtn.bind("click", function()
				{
					var downloadState = $(this).attr("state");
					var appInfo = eval("(" + $(this).parent().attr("data-json") + ")");
					switch(parseInt(downloadState))
					{
					case a.downState.pause[2]:
					
						$(this).attr("state", a.downState.downloading[2]);
						$(this).attr("title", a.downState.downloading[1]);
						$(this).text(a.downState.downloading[0]);

					 	external.ResumeDownload(appInfo.download_url);
						break
					case a.downState.downloading[2]:
			
						$(this).attr("state", a.downState.pause[2]);
						$(this).attr("title", a.downState.pause[1]);
						$(this).text(a.downState.pause[0]);
						external.PauseDownload(appInfo.download_url);
						break;
					case a.downState.ok[2]:
				
						$(this).attr("state", a.downState.downloading[2]);
						$(this).attr("title", a.downState.downloading[1]);
						$(this).text(a.downState.downloading[0]);
						external.BeginShareDownload2(appInfo.download_url,appInfo.title + ".ipa", appInfo.package_name, appInfo.appid);
						break;
					default:
						$(this).attr("state", a.downState.downloading[2]);
						$(this).attr("title", "点击下载");
						$(this).text(a.downState.downloading[0]);
						external.BeginShareDownload2(appInfo.download_url,appInfo.title + ".ipa", appInfo.package_name, appInfo.appid);
						break
					}
			
				});		
	};
	a.downBtnCallback = function(ab, b, c)
	{
		for(var i = 0; i < a.downBtn.size(); i++){
			var downloadBtn = a.downBtn.eq(i);
			var appInfo = eval("(" + downloadBtn.parent().attr("data-json") + ")");

			if(appInfo.download_url == ab)
			{
				downloadBtn.attr("state",b);
				switch(b)
				{
				case a.downState.pause[2]:
					downloadBtn.text(a.downState.pause[0]);
					downloadBtn.attr("title", a.downState.pause[1]);
					//a.disableSetupBtn(downloadBtn, 0);
					break;
				case a.downState.downloading[2]:
					downloadBtn.text(a.downState.downloading[0]);
					downloadBtn.attr("title", a.downState.downloading[1]);
					//a.disableSetupBtn(downloadBtn, 0);
					break;
				case a.downState.ok[2]:
					downloadBtn.text(a.downState.ok[0]);
					downloadBtn.attr("title", a.downState.ok[1]);
					//a.disableSetupBtn(downloadBtn, 1);
					break;
				case 51:
					if(1 == downloadBtn.prev().attr("state"))
					{
						a.updateSetupBtn();
					}	
				default:
					downloadBtn.text(a.downState.begin[0]);
					downloadBtn.attr("title", "点击下载");
					break 
				
				}
				//break;	//?????
			}
		}
	};
	
	a.downBtnUpdate = function()
	{
		var downInfo = eval("(" + external.GetDownloadInfo(-1) + ")").result;
		
		for(var i = 0; i <  a.downBtn.size(); i++)
		{
			
			var downloadBtn = a.downBtn.eq(i);
			
			downloadBtn.attr("state", a.downState.begin[2]);
        	downloadBtn.text(a.downState.begin[0]);
        	downloadBtn.attr("title", a.downState.begin[1]);
        	
			var appInfo = eval("(" + downloadBtn.parent().attr("data-json") + ")");
			
			for (var j = 0; j < downInfo.length; j++) 
			{
				if(downInfo[j][0] == appInfo.download_url)
				{
					 switch (downInfo[j][1]) {
	                    case a.downState.downloading[2]: 
	                    	downloadBtn.attr("state", a.downState.downloading[2]);
	                    	downloadBtn.text(a.downState.downloading[0]);
	                    	downloadBtn.attr("title", a.downState.downloading[1]);
							//a.disableSetupBtn(downloadBtn, 0);
	                        break;
	                    case a.downState.pause[2]:
	                    	downloadBtn.attr("state", a.downState.pause[2]);
	                    	downloadBtn.text(a.downState.pause[0]);
	                    	downloadBtn.attr("title", a.downState.pause[1]);
							//a.disableSetupBtn(downloadBtn, 0);
	                        break;
	                    case a.downState.ok[2]:
	                    	downloadBtn.attr("state", a.downState.ok[2]);
	                    	downloadBtn.attr("title", a.downState.ok[1]);
	                    	downloadBtn.text(a.downState.ok[0]);
							//a.disableSetupBtn(downloadBtn, 1);
	                        break;
	                    default:
	                    	//downloadBtn.attr("state", a.downState.begin[2]);
	                    	//downloadBtn.text(a.downState.begin[0]);
	                        break
	                    }
					 break;
				}
			}
		}
	};
	
	a.disableSetupBtn = function(btn, lable)
	{
		var setupBtn = btn.prev();
		if(lable == 1)
		{
			if(setupBtn.attr("state") == 1)
			{
				setupBtn.text("安装中");
				setupBtn.attr("title", "安装中..");				
			}else
			{
				setupBtn.attr("disabled",false);		
				setupBtn.toggleClass("no",false);
				return;
			}
			
		}else
		{
			setupBtn.text("下载中");
			setupBtn.attr("title", "正在下载..");
		}
		
		setupBtn.attr("disabled",true);		
		setupBtn.toggleClass("no",true);
	};	
})(cc_pc_ios);


$(document).ready(function() {
    document.ondragstart = function() {
        return false
    };
    cc_pc_ios.init(".app-install-btn-js",".app-download-btn-js");
});

var getDeviceJson = cc_pc_ios.getDeviceJsonInfo;
var downloadStateChanged = cc_pc_ios.downBtnCallback;