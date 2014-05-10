//浏览器宽度自适应
$(document).ready(function(e) {
	  resize(); 
	  $(window).resize(function() {
		resize();
	  });
});
function resize(){
	var width = $(window).width();
	var wobj = $("body");
	if(width > 1250){
		wobj.attr("id","cc-l");	
	}else if(width > 990){
		wobj.attr("id","cc-m");	
	}else{
		wobj.attr("id","cc-s");	
	}
};


document.writeln("<a href=\"javascript:;\" title=\"我要许愿\" id=\"go-wish\">我要许愿</a>");
document.writeln("<style>#toTop{width:44px;height:44px;position:fixed;right:20px;bottom:-10px;z-index:9999;display:none;text-indent:-9999px;background:url(http://static.ccplay.com.cn/static/common/img/go-top.png) no-repeat}#toTop:hover{background-position:left bottom}</style>");
document.writeln("<a href=\"javascript:;\" title=\"返回顶部\" id=\"toTop\">返回顶部</a>");
$(document).ready(function(){
	$(window).scroll(function(){
		if($(window).scrollTop()<=0) {
			$("html").attr("ID","");
		}else{
			$("html").attr("ID","fixed-head");
		}
		
		if($(window).scrollTop()<=500) {
			$("#toTop").stop(true,false).animate({bottom:"-10px",opacity:"0"},50);
		}else{
			$("#toTop").stop(true,false).show().animate({bottom:"20px",opacity:"1"},50);
		}
	});
	$("#toTop").click(function(){
		$("body,html").animate({scrollTop:0},200);
	});
});

//评分
$(document).ready(function(){
	// hover
	$('#rating_btns li').hover(function(){	
			$rating = $(this).text();
			$('#rating_on').css('width', rateWidth($rating));
	});		
	// mouseout
	$('#rating_btns li').mouseout(function(){
	
		$rating = $('#rating').text();
		if($rating == ""){		
			$('#rating_on').css('width', "0px");
		}
		else{
			$('#rating_on').css('width', rateWidth($rating));	
		}
	});	
	//click
	$('#rating_btns li').click(function(){
		$rating = $(this).text();		
//		$r_text = $(this).attr("title");		
//		$('#rating').text($r_text);		
		$('#rating').text($rating+'分');
		$('#rating_output').val($rating);
		$pos = starSprite($rating);
	});	
	function rateWidth($rating){		
		$rating = parseFloat($rating);
		switch ($rating){
			case 1: $width = "25px"; break;
			case 2: $width = "54px"; break;
			case 3: $width = "81px"; break;
			case 4: $width = "107px"; break;
			case 5: $width = "134px"; break;
			default:  $width =  "0";
		}
		return $width;
	}
});	



$(function(){
	
$(".app-list-m a,.app-list-xl a,.app-list-l a,.app-list-min a,.hot-bbs-list a,.novice-bbs-list a,.i-link-list a").attr("target","_blank");
	
//搜索
	$(".search").hover(function(){
		$(this).find(".box").addClass("hover");
	},function(){
		$(this).find(".box").removeClass("hover");
	});	
//搜索提示
	$(".key").keyup(function(){
		var inputvalue = $(".key").val();
		if(inputvalue  != ""){
			$('#search-drop').show().animate({opacity:"1"},200);
		}else if(inputvalue == ""){
			$("#n_l_closbtn").hide();
		}
	});	
	$(document).ready(function(e) {
	   var inputvalue = $(".key").val();
		if(inputvalue  != ""){
			$('#search-drop').show().animate({opacity:"1"},200);
		}else if(inputvalue == ""){
			$('#search-drop').hide().animate({opacity:"0"},200);
		}
	});
	$('.key').blur(function(){
		$('#search-drop').hide().animate({opacity:"0"},200);
	});
//微信
	$(".weixin-code,#cc-s .down-btn,#cc-m .down-btn").hover(function(){
       $(this).find("img").fadeIn(300);
	 }, function(){
	   $(this).find("img").fadeOut(300);
	 });


//安装 下载按钮
	function li_btn(eobj,cssClass){
		eobj.hover(function(){		  
		   $(this).find(cssClass).show();
		},function(){
			 $(this).find(cssClass).hide();
		});
	};	
	li_btn($(".app-list-min,.app-list-xl,.maste_lsit"),".btn-s");
	li_btn($(".sort"),".sort-menu");
	li_btn($(".box_btn,.collection_box"),".a_btn");	
	li_btn($(".logo .rel"),".home");	
	
//首个APP展开	
	function li_hover(eobj,cssClass){
		eobj.hover(function(){
		   $(this).siblings().removeClass(cssClass);
		   $(this).addClass(cssClass);
		});
	};	
	li_hover($(".app-list-right li"),"hover");	
	li_hover($(".t-title li"),"ios-web-icon");	
	
	$(".app-list-right").find("li:first").addClass("hover");
	$(".hot-bbs .hot-bbs-list").find("li:first").addClass("first");
	
//基本资料-表单验证
	var info=$(".user-info-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:true,
		//ajaxPost:true
	});	
	info.addRule([{
		ele:".w200:eq(0)",datatype:"*1-16"},{
		ele:".w200:eq(1)",ignore:"ignore",datatype:"zh2-4"},{
		ele:"select:eq(0)",datatype:"*"},{
		ele:"select:eq(1)",datatype:"*"},{
		ele:"select:eq(2)",datatype:"*"},{
		ele:":radio:first",	datatype:"*"}
	]);

//联络信息-表单验证
	var contact=$(".user-contact-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:true,
		//ajaxPost:true
	});	
	contact.addRule([{
		ele:".w200:eq(4)",datatype:"*"}
	]);


//修改密码-表单验证
	var password=$(".user-password-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:true,	
		//ajaxPost:true
	});	
	password.addRule([{
		ele:".w200",datatype:"*6-16"},{
		ele:".w200:eq(2)",datatype:"*6-16",recheck:"new_password"}
	]);
	
//注册表单-表单验证
	var reg=$(".reg-form").Validform({
		showAllError:true,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".login-tip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		},
		//ajaxPost:true
	});

//登录表单-表单验证
	var reg=$(".login-form").Validform({
		showAllError:true,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".login-tip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		},
		//ajaxPost:true
	});

	

//我要许愿-表单验证
	var wish=$(".go-wish-form").Validform({
		showAllError:true,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".Validform_checktip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		}
	});	
	wish.addRule([{
		ele:".pct50",datatype:"*"}
	]);
	


});








/*----------密码强度-----------*/
function check_password_strong ( password )
{

	var strong = get_strong_level ( password, 6 );

	var objS = document.getElementById ( 'pw-strength' );

	if ( strong <=35 && strong > 0 )
	{
		objS.className = 'abs g9 dib pw-1';
	}
	else if ( strong > 35 && strong < 65 )
	{
		objS.className = 'abs g9 dib pw-2';
	}
	else if ( strong >=65 )
	{
		objS.className = 'abs g9 dib pw-3';
	}
	else
	{
		objS.className = 'abs g9 dn';
	}
}

function get_strong_level ( string, minLength )
{
	if ( minLength == null ) minLength = 1;
	if ( string.length < minLength )
	{
		return 0;
	}
	var ls = 0;
	if ( string.match(/([!@#$%^&*()_+\-]+)/ig ) )
	{
		ls += 40;
	}
	if ( string.match(/([a-z])/ig ) )
	{
		ls += 20;
	}
	if ( string.match(/([0-9])/ig ) )
	{
		ls += 20;
	}
	return ls;
}




//banner
$(".banner").slide({ titCell:".num ul" , mainCell:".ban_pic ul" , autoPlay:true, effect:"fold",delayTime:1500 , autoPage:true });

//专题 巨作
jQuery(".roll").slide({ mainCell:"ul",vis:3,scroll:3,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});

//详细缩略图
jQuery(".up_box").slide({ mainCell:"ul",vis:0,scroll:2,prevCell:".prev",nextCell:".next",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//专题页
jQuery(".collection_box").slide({ mainCell:".inner-box",vis:0,scroll:1,prevCell:".prev",nextCell:".next",easing:"easeInQuint",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//游戏排行榜
jQuery(".tab-box").slide({ titCell:".info-tag a",mainCell:".info-box-tab" });



//固定APP分类菜单
//$(".nav").pin()
$(".pin-box").pin({
      containerSelector: ".width"//固定到某个DIV范围内
});






//滑动TBA
//var TabbedContent = {
//	init: function() {	
//		$(".tab").mouseover(function() {		
//			var background = $(this).parent().find(".ios-web-icon");	
//			$(background).animate({
//				left: $(this).position()['left']
//			}, {
//				duration: 300
//			});		
//		});
//	}
//}
//$(document).ready(function() {
//	TabbedContent.init();
//});





//placeholder
var funPlaceholder = function(element) {
    var placeholder = '';
    if (element && !("placeholder" in document.createElement("input")) && (placeholder = element.getAttribute("placeholder"))) {
        element.onfocus = function() {
            if (this.value === placeholder) {
                this.value = "";
            }
            this.style.color = '#333';
        };
        element.onblur = function() { 
            if (this.value === "") {
                this.value = placeholder;
                this.style.color = '#ccc';    
            }
        };
        
        //样式初始化
        if (element.value === "") {
            element.value = placeholder;
            element.style.color = '#ccc';    
        }
    } 
};
funPlaceholder(document.getElementById("p-id"));
funPlaceholder(document.getElementById("p-pw"));
funPlaceholder(document.getElementById("p-yzm"));

funPlaceholder(document.getElementById("p-password"));
funPlaceholder(document.getElementById("p-password2"));
funPlaceholder(document.getElementById("p-new_password"));
funPlaceholder(document.getElementById("p-new_password2"));
funPlaceholder(document.getElementById("p-email"));

funPlaceholder(document.getElementById("wish-game-name"));
funPlaceholder(document.getElementById("wish-game-ver"));
funPlaceholder(document.getElementById("wish-game-type"));
funPlaceholder(document.getElementById("wish-game-note"));






//弹窗
$(function(){	
		//登录
		$(".open-login").click(function(){
			$(".login-box").zxxbox({
				title: "会员登录"	,fix: true
				});
		});
		//注册
		$(".open-reg").click(function(){
			$(".reg-box").zxxbox({
				title: "用户注册"	 ,fix: true
				});
		});
		//许愿
		$("#go-wish").click(function(){
			$(".go-wish-box").zxxbox({
				title: "我要许愿"	 ,fix: true
				});
		});
		
		
		
		
	//提示
	$("#win").click(function(){
    $.zxxbox('<div class="p20 f20 white tc"><i class="icon-ok-circle mr10 f28"></i><span class="dib rel">操作成功！</span></div>', {
        delay: 2000, bar: false, bg: false, fix: true
//		   	,
//		     onclose: function(){ 
//            window.location.href='baidu.com';  // √
//            }
        });							
    });	
//<div class="p20 f20 white"><i class="icon-remove-circle mr10 f28"></i><span class="dib rel">操作失败！</span></div>
//<div class="p20 f20 white"><i class="icon-exclamation-sign mr10 f28"></i><span class="dib rel">出错啦~</span></div>
//<div class="p20 f20 white"><i class="icon-minus-sign mr10 f28"></i><span class="dib rel">禁止！~</span></div>
	
	//询问
	$("#box_remind").click(function(){
    $.zxxbox.remind('<span class="db pb15 f16">请输入您注册的电子邮箱，下一步将发送修改密码链接到该邮箱。</span><input class="pct50 bg-white pl10 bg-white bde pt10 pb10 f16" type="text" placeholder="请输入电子邮箱" id="p-email" datatype="e">', function(){
        //alert("哇哈哈");
    }, {
        title: "找回密码"	 ,bg: true, fix: true, bgclose:true
    });						   
	});
	
	

	
	
	
	
	$("#box_ask").click(function(){
    $.zxxbox.ask('<span class="f16 tc">文字内字文字内容区域文字内容区域文字内容区域文<br/>字内容区域文字内容区域文字内容区域文字内容区域文字内容区域，<br/>支持HTML 支持HTML 支持HTML</span>', function(){
        $("body").css("background-color", "azure");	
    }, null, {
        title: "友情提示"	,bg: true, fix: true, bgclose:true
    });						   
	});	
	
	$("#sub1").click(function(){
		$.zxxbox($("#box"), {
        title: "标题"	
        });
    });
	
	
	
	
	
});



//许愿
document.writeln("<div class=\"bg-white go-wish-box dn\">");
document.writeln("<form class=\"w750 fw go-wish-form\">");
document.writeln("<div class=\"pb20\">");
document.writeln("<input class=\"pct50 bg-white pl10 bg-white bde pt10 pb10 f16 mb10\" type=\"text\" placeholder=\"游戏名称\" id=\"wish-game-name\"><span class=\"g9 ml10\">如：暗影之刃 Shadow Blade</span>");
document.writeln("<input class=\"pct50 bg-white pl10 bg-white bde pt10 pb10 f16 mb10\" type=\"text\" placeholder=\"版本编号\" id=\"wish-game-ver\"><span class=\"g9 ml10\">如：v1.14.2</span>");
document.writeln("<input class=\"pct50 bg-white pl10 bg-white bde pt10 pb10 f16 mb10\" type=\"text\" placeholder=\"破解类型\" id=\"wish-game-type\"><span class=\"g9 ml10\">如：无限金币/无限道具/内购/强制购买/免验证等</span>");
document.writeln("<input class=\"pct50 bg-white pl10 bg-white bde pt10 pb10 f16\" type=\"text\" placeholder=\"备注\" id=\"wish-game-note\"><span class=\"g9 ml10\">对虫虫游戏说的话~</span>");
document.writeln("</div>");
document.writeln("<div class=\"db tr pt20 pb20\">");
document.writeln("<span class=\"Validform_checktip\"></span><button class=\"submit_btn\">提交许愿</button>");
document.writeln("</div>");
document.writeln("</form>");
document.writeln("</div>");

//弹出框提示 结束







//搜索选择
function diy_select(){this.init.apply(this,arguments)};
diy_select.prototype={
	 init:function(opt)
	 {
		this.setOpts(opt);
		this.o=this.getByClass(this.opt.TTContainer,document,'div');//容器
		this.b=this.getByClass(this.opt.TTDiy_select_btn);//按钮
		this.t=this.getByClass(this.opt.TTDiy_select_txt);//显示
		this.l=this.getByClass(this.opt.TTDiv_select_list);//列表容器
		this.ipt=this.getByClass(this.opt.TTDiy_select_input);//列表容器
		this.lengths=this.o.length;
		this.showSelect();
	 },
	 addClass:function(o,s)//添加class
	 {
		o.className = o.className ? o.className+' '+s:s;
	 },
	 removeClass:function(o,st)//删除class
	 {
		var reg=new RegExp('\\b'+st+'\\b');
		o.className=o.className ? o.className.replace(reg,''):'';
	 },
	 addEvent:function(o,t,fn)//注册事件
	 {
		return o.addEventListener ? o.addEventListener(t,fn,false):o.attachEvent('on'+t,fn);
	 },
	 showSelect:function()//显示下拉框列表
	 {
		var This=this;
		var iNow=0;
		this.addEvent(document,'click',function(){
			 for(var i=0;i<This.lengths;i++)
			 {
				This.l[i].style.display='none';
			 }
		})
		for(var i=0;i<this.lengths;i++)
		{
			this.l[i].index=this.b[i].index=this.t[i].index=i;
			this.t[i].onclick=this.b[i].onclick=function(ev)  
			{
				var e=window.event || ev;
				var index=this.index;
				This.item=This.l[index].getElementsByTagName('li');

				This.l[index].style.display= This.l[index].style.display=='block' ? 'none' :'block';
				for(var j=0;j<This.lengths;j++)
				{
					if(j!=index)
					{
						This.l[j].style.display='none';
					}
				}
				This.addClick(This.item);
				e.stopPropagation ? e.stopPropagation() : (e.cancelBubble=true); //阻止冒泡
			}
		}
	 },
	 addClick:function(o)//点击回调函数
	 {

		if(o.length>0)
		{
			var This=this;
			for(var i=0;i<o.length;i++)
			{
				o[i].onmouseover=function()
				{
					This.addClass(this,This.opt.TTFcous);
				}
				o[i].onmouseout=function()
				{
					This.removeClass(this,This.opt.TTFcous);
				}
				o[i].onclick=function()
				{
					var index=this.parentNode.index;//获得列表
					This.t[index].innerHTML=This.ipt[index].value=this.innerHTML.replace(/^\s+/,'').replace(/\s+&/,'');
					This.l[index].style.display='none';
				}
			}
		}
	 },
	 getByClass:function(s,p,t)//使用class获取元素
	 {
		var reg=new RegExp('\\b'+s+'\\b');
		var aResult=[];
		var aElement=(p||document).getElementsByTagName(t || '*');

		for(var i=0;i<aElement.length;i++)
		{
			if(reg.test(aElement[i].className))
			{
				aResult.push(aElement[i])
			}
		}
		return aResult;
	 },

	 setOpts:function(opt) //以下参数可以不设置  //设置参数
	 { 
		this.opt={
			 TTContainer:'diy_select',//控件的class
			 TTDiy_select_input:'diy_select_input',//用于提交表单的class
			 TTDiy_select_txt:'diy_select_txt',//diy_select用于显示当前选中内容的容器class
			 TTDiy_select_btn:'diy_select_txt',//diy_select的打开按钮
			 TTDiv_select_list:'diy_select_list',//要显示的下拉框内容列表class
			 TTFcous:'focus'//得到焦点时的class
		}
		for(var a in opt)  //赋值 ,请保持正确,没有准确判断的
		{
			this.opt[a]=opt[a] ? opt[a]:this.opt[a];
		}
	 }
}

var TTDiy_select=new diy_select({  //参数可选
});//如同时使用多个时请保持各class一致.



	





//邮箱地址自动完成
(function($) {
	$.fn.mailAutoComplete = function(options) {
		var defaults = {
			className: "emailist bdc bg-white lh28 poi",
			email: 	["qq.com","gmail.com","126.com","163.com","hotmail.com","live.nc","sohu.com","sina.com.cn"], //邮件数组
			zIndex: 2	
		};
		// 最终参数
		var params = $.extend({}, defaults, options || {});
		
		// 是否现代浏览器
		var isModern = typeof window.screenX === "number", visibility = "visibility";
		// 键值与关键字
		var key = {
			"up": 38,
			"down": 40,
			"enter": 13,
			"esc": 27,
			"tab": 9	
		};
		// 组装HTML的方法
		var fnEmailList = function(input) {
			var htmlEmailList = '', arrValue = input.value.split("@"), arrEmailNew = [];
			$.each(params.email, function(index, email) {
				if (arrValue.length !== 2 || arrValue[1] === "" || email.indexOf(arrValue[1].toLowerCase()) === 0) {			
					arrEmailNew.push(email);						
				}
			});	
			$.each(arrEmailNew, function(index, email) {
				htmlEmailList = htmlEmailList + '<li'+ (input.indexSelected===index? ' class="on"':' class="pt2 pb2 pl10"') +'>'+ arrValue[0] + "@" + email +'</li>';	
			});		
			return htmlEmailList;			
		};
		// 显示还是隐藏
		var fnEmailVisible = function(ul, isIndexChange) {
			var value = $.trim(this.value), htmlList = '';
			if (value === "" || (htmlList = fnEmailList(this)) === "") {
				ul.css(visibility, "hidden");	
			} else {
				isIndexChange && (this.indexSelected = -1);
				ul.css(visibility, "visible").html(htmlList);
			}
		};
		
		return $(this).each(function() {
			this.indexSelected = -1;
			// 列表容器创建
			var element = this;
			var eleUl = $('<ul></ul>').css({
				position: "absolute",
				marginTop: element.offsetHeight,
				minWidth: element.offsetWidth - 2,
				visibility: "hidden",
				zIndex: params.zIndex
			}).addClass(params.className).bind("click", function(e) {
				var target = e && e.target;
				if (target && target.tagName.toLowerCase() === "li") {
					$(element).val(target.innerHTML).trigger("input");
					$(this).css(visibility, "hidden");
					element.focus(); // add on 2013-11-20
				}				
			});			
			$(this).before(eleUl);
			// IE6的宽度
			if (!window.XMLHttpRequest) { eleUl.width(element.offsetWidth - 2); }	
			
			// 不同浏览器的不同事件
			isModern? $(this).bind("input", function() {
				fnEmailVisible.call(this, eleUl, true);
			}): element.attachEvent("onpropertychange", function(e) {				
				if (e.propertyName !== "value") return;
				fnEmailVisible.call(element, eleUl, true);		
			});
			
			$(document).bind({
				"click": function(e) {
					var target = e && e.target, htmlList = '';
					if (target == element && element.value && (htmlList = fnEmailList(element, params.email))) {
						eleUl.css(visibility, "visible").html(htmlList);	
					} else if (target != eleUl.get(0) && target.parentNode != eleUl.get(0)) {
						eleUl.css(visibility, "hidden");
					}
				},
				"keydown": function(e) {
					var eleLi = eleUl.find("li");
					if (eleUl.css(visibility) === "visible") {
						switch (e.keyCode) {
							case key.up: {
								element.indexSelected--;
								if (element.indexSelected < 0) {
									element.indexSelected = -1 + eleLi.length;	
								}
								e.preventDefault && e.preventDefault();
								break;
							}
							case key.down: {
								element.indexSelected++;
								if (element.indexSelected >= eleLi.length) {
									element.indexSelected = 0;	
								}
								e.preventDefault && e.preventDefault();
								break;
							}
							case key.enter: {		
								e.preventDefault();		
								eleLi.get(element.indexSelected) && $(element).val(eleLi.eq(element.indexSelected).html());
								eleUl.css("visibility", "hidden");
								break;
							}
							case key.tab: case key.esc: {
								eleUl.css("visibility", "hidden");
								break;
							}
						}
						if (element.indexSelected !== -1) {
							eleUl.html(fnEmailList(element));
						}
					}
				}
			});		
		});
	};
})(jQuery);
$("#p-email").mailAutoComplete();




