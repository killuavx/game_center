//浏览器宽度自适应
$(document).ready(function(e) {
	  resize(); 
	  $(window).resize(function() {
		resize();
	  });
	  
	  //最小高度
	  var screen_height = $(window).height();
	  var head_height = $('.head').outerHeight(true);  
	  var foot_height = $('.footer').outerHeight(true);
	  var $body = $('.minheight-page');
	  if ($body.size()) {
		var bodyMarginTop = $body.css("marginTop").replace('px', '');
		var bodyMarginBottom = $body.css("marginBottom").replace('px', '');  
		var body_height = screen_height - head_height - foot_height - bodyMarginTop - bodyMarginBottom;  
		$body.css('min-height', body_height + 'px');
	  }

});

/*
 * app详情图片事件绑定
*/

var imgloadCount = 0;
function bindAppDetailCoverEv(vis_count){

	var e = $(".up_pic img");
	var imageCount = e.size();
	
	if(imgloadCount == 0){
	
		e.each(function(){
			if(this.complete){
				imgloadCount++
			}
		});
		
		if(imgloadCount == imageCount){
			jQuery(".up_box").slide({ mainCell:"ul",vis:vis_count,scroll:vis_count,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		}else{
			e.load(function(){
				imgloadCount++;
				if(imgloadCount == imageCount){
					jQuery(".up_box").slide({ mainCell:"ul",vis:vis_count,scroll:vis_count,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
				}
			});
		}
	}else{
		jQuery(".up_box").slide({ mainCell:"ul",vis:vis_count,scroll:vis_count,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		
	}	
}

function resize(){
	var width = $(window).width();
	var wobj = $("body");
	if(width > 1250){
		wobj.attr("id","cc-l");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:5,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:4,scroll:4,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(4);
	}else if(width > 990){
		wobj.attr("id","cc-m");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:4,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:3,scroll:3,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(3);

	}else{
		wobj.attr("id","cc-s");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:3,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:2,scroll:2,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(2);

	}
};

//document.writeln("<a href=\"javascript:;\" title=\"我要许愿\" id=\"go-wish\">我要许愿</a>");

//返回顶部
document.writeln("<style>#toTop{width:44px;height:44px;position:fixed;right:20px;bottom:-10px;z-index:9999;display:none;text-indent:-9999px;background:url(http://static.ccplay.com.cn/static/common/img/go-top.png) no-repeat}#toTop:hover{background-position:left bottom}</style>");
document.writeln("<a href=\"javascript:;\" title=\"返回顶部\" id=\"toTop\">返回顶部</a>");
$(document).ready(function(){
	var index = 0;
	var _window = $(window);
	var _html = $("html");
	var _toTop = $("#toTop");
	$(window).scroll(function(){
		/*var currentIndex = _window.scrollTop();
		if(currentIndex > index){
			_html.attr("ID","");
		}else{
			_html.attr("ID","fixed-head");
		}
		index = currentIndex;*/
		
		if($(window).scrollTop()<=0) {
			_html.attr("ID","");
		}else{
			_html.attr("ID","fixed-head");
		}
		
		if($(window).scrollTop()<=500) {
			_toTop.stop(true,false).animate({bottom:"-10px",opacity:"0"},50);
		}else{
			_toTop.stop(true,false).show().animate({bottom:"20px",opacity:"1"},50);
		}
	});
	$("#toTop").click(function(){
		$("body,html").animate({scrollTop:0},200);
	});
});




$(function(){

//搜索
	$(".search").hover(function(){
		$(this).find(".box").addClass("hover");
	},function(){
		$(this).find(".box").removeClass("hover");
	});	
//搜索框
	var sea=$(".search").Validform({
		//tiptype:3,
		tipSweep:true
	});	
	sea.addRule([{
		ele:".key",datatype:"*"}
	]);
//搜索提示
	/*$(".key").keyup(function(){		
		var inputvalue = $(".key").val();
		if(inputvalue  != ""){
			$('#search-drop').show().animate({opacity:"1"},200);
		}else if(inputvalue == ""){
			$("#search-drop").hide().animate({opacity:"0"},200);
		};		
	});		
	
	$('.key').blur(function(){
		$('#search-drop').hide().animate({opacity:"0"},200);
	});*/
	
	//登录后
	jQuery(".user-switch").slide({ type:"menu", titCell:"li", targetCell:"dl", delayTime:300, triggerTime:0,returnDefault:true  });
	//.change-password
	//.log-out	
	
	$(".change-password").click(function(){
		$.zxxbox($(".change-password-box"), {
        title: "修改密码"	, fix: true
        });
    });
	
	
    /*
	$(".log-out").click(function(){
    	$.zxxbox('<div class="p20 f20 white tc">安全退出成功！</span></div>', {delay: 2000, bar: false, bg: false, fix: true});							
    }); */
	
	
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
	
//首个APP展开	
	function li_hover(eobj,cssClass){
		eobj.hover(function(){
		   $(this).siblings().removeClass(cssClass);
		   $(this).addClass(cssClass);
		});
	};	
	li_hover($(".app-list-right li"),"hover");	
	
	$(".app-list-right").find("li:first").addClass("hover");
	
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

//密码加强
(function(a){a.fn.passwordStrength=function(b){b=a.extend({},a.fn.passwordStrength.defaults,b);this.each(function(){var d=a(this),e=0,c=false,f=a(this).parents("form").find("#pw-strength");d.bind("keyup blur",function(){e=a.fn.passwordStrength.ratepasswd(d.val(),b);e>=0&&c==false&&(c=true);f.find("span").removeClass("gr");if(e<35&&e>=0){f.find("span:first").addClass("gr")}else{if(e<60&&e>=35){f.find("span:lt(2)").addClass("gr")}else{if(e>=60){f.find("span:lt(3)").addClass("gr")}}}if(c&&(d.val().length<b.minLen||d.val().length>b.maxLen)){b.showmsg(d,d.attr("errormsg"),3)}else{if(c){b.showmsg(d,"",2)}}b.trigger(d,!(e>=0))})})};a.fn.passwordStrength.ratepasswd=function(c,d){var b=c.length,e;if(b>=d.minLen&&b<=d.maxLen){e=a.fn.passwordStrength.checkStrong(c)}else{e=-1}return e/4*100};a.fn.passwordStrength.checkStrong=function(d){var e=0,b=d.length;for(var c=0;c<b;c++){e|=a.fn.passwordStrength.charMode(d.charCodeAt(c))}return a.fn.passwordStrength.bitTotal(e)};a.fn.passwordStrength.charMode=function(b){if(b>=48&&b<=57){return 1}else{if(b>=65&&b<=90){return 2}else{if(b>=97&&b<=122){return 4}else{return 8}}}};a.fn.passwordStrength.bitTotal=function(b){var d=0;for(var c=0;c<4;c++){if(b&1){d++}b>>>=1}return d};a.fn.passwordStrength.defaults={minLen:0,maxLen:30,trigger:a.noop}})(jQuery);


//修改密码-表单验证
	var password=$(".user-password-form").Validform({
		tiptype:3,
		usePlugin:{
			passwordstrength:{minLen:6,maxLen:16}
		},
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
		usePlugin:{
			passwordstrength:{minLen:6,maxLen:16}
		},
		tiptype:function(msg,o,cssctl){
			var objtip=$(".login-tip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		},
		ajaxPost:true,
        callback: function(data){
            if(data.code == 0){
                window.location.href = data.next
            }
            else
            {
                var msgs = [];
                for(k in data.errors)
                {
                    msgs.push(data.errors[k].join(','));
                }
                alert(msgs.join(','));
                refresh_captcha('.yzm-img');
            }
        }
	});

//登录表单-表单验证
	var reg=$(".login-form").Validform({
		showAllError:true,	
		ajaxPost:true,
        btnSubmit: '.login-btn',
        callback: function(data){
            window.test = data;
            console.log(data);
            if(data.code == 0){
                $.zxxbox.hide();
                $('.login-form').remove();
                window.location.reload();
            }
            else
            {
                var msgs = [];
                for(k in data.errors)
                {
                    msgs.push(data.errors[k].join(','));
                }
                alert(msgs.join(','));
                refresh_captcha('.yzm-img');
            }
        }
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

//评论
    var comment_tips = $('#comments .comment-tip');
    var review=$(".comment-form").Validform({
        showAllError:true,
        tiptype:function(msg,o,cssctl){
            var objtip=$("");
            cssctl(comment_tips,o.type);
            objtip.text(msg);
        },
        ajaxPost:true,
        callback: function(data){
            if( data.code == 0 )
            {
                comment_tips.html('');
                page_load($('#comment-list .page'), 1);
                $('.comment-form textarea[name=comment]').val('');
                $('.comment-form input[name=rating_output]').val('');
                $('#rating_on').attr('style', '');
                alert(data.msg);
            }
            else
            {
                var msgs = [];
                for(k in data.errors)
                {
                    msgs.push(data.errors[k].join(','));
                }
                var _msg = data.msg + " " + msgs.join(", ")
                comment_tips.html(_msg);
            }
            return false;
        }
    });
	review.addRule([{
		ele:".comment-box",datatype:"*1-300"}
	]);		


});



//banner
$(".banner").slide({ titCell:".num ul" , mainCell:".ban_pic ul" , autoPlay:true, autoPage:true });

/*合集页*/
jQuery(".collection_box").slide({ mainCell:".inner-box",vis:3,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});

/*游戏*/
jQuery(".tab-box").slide({ titCell:".info-tag a",mainCell:".info-box-tab"});

/*游戏排行榜*/
jQuery(".tab-box-o").slide({ titCell:".t-title li",mainCell:".info-box-tab",targetCell:".tab-more a", titOnClassName:"ios-web-icon"});



/*固定APP分类菜单*/
/*$(".nav").pin()*/
$(".pin-box").pin({
      containerSelector: ".width"/*固定到某个DIV范围内*/
});





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
		//关于我们
		$("#about").click(function(){
			$("#about-box").zxxbox({
				title: "关于我们"	 ,fix: true, bgclose:true
				});
		});
		//发展愿景
		$("#vision").click(function(){
			$("#vision-box").zxxbox({
				title: "发展愿景"	 ,fix: true, bgclose:true
				});
		});
		//联系方式
		$("#contact").click(function(){
			$("#contact-box").zxxbox({
				title: "联系方式"	 ,fix: true, bgclose:true
				});
		});
		
		
		
		
	//提示
	$("#win").click(function(){
    $.zxxbox('<div class="p20 f20 white tc">操作成功！</span></div>', {
        delay: 2000, bar: false, bg: false, fix: true
//		   	,
//		     onclose: function(){ 
//            window.location.href='baidu.com';  // √
//            }
        });							
    });
	
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
/*document.writeln("<div class=\"bg-white go-wish-box dn\">");
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
document.writeln("</div>");*/
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
		});
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
					This.t[index].innerHTML=this.innerHTML.replace(/^\s+/,'').replace(/\s+&/,'');
                    This.ipt[index].value=this.getAttribute('data');
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
			 TTDiy_select_btn:'diy_select_btn',
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



//评分
$(document).ready(function(){
	$('#rating_btns li').hover(function(){	
			$rating = $(this).text();
			$('#rating_on').css('width', rateWidth($rating));
	},function(){
		 $rating = $('#rating').text();
		if($rating == ""){		
			 $('#rating_on').css('width', "0px");
		 }
		 else{
			 $('#rating_on').css('width', rateWidth($rating));	
		 }
	});
	$('#rating_btns li').click(function(){
		$rating = $(this).text();			
		$('#rating').text($rating+'分');
		$('#rating_output').val($rating);
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