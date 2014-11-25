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
			jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		}else{
			e.load(function(){
				imgloadCount++;
				if(imgloadCount == imageCount){
					jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
				}
			});
		}
	}else{
		jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		
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




/*返回顶部*/
document.writeln("<div class=\"auto width aside-float-bar\" id=\"aside-float-bar\"><ul><li class=\"bdsharebuttonbox\"><a href=\"javascript:;\"class=\"bds_more a-share\"data-cmd=\"more\">分享游戏</a></li><li class=\"li_code\"><a href=\"#\"class=\"a-qr-code\"title=\"二维码\"></a><div class=\"qr-code-box\"><dl><dd><img src=\"http://static.ccplay.com.cn/static/android_web/img/weixin-code.png\"/></dd><dt>关注微信<br/>虫虫游戏助手</dt></dl><dl><dd><img src=\"http://static.ccplay.com.cn/static/android_web/img/weibo-code.png\"/></dd><dt><u class=\"tdl poi\"onClick=\"window.open(\'http://weibo.com/ccyxpt\')\">新浪微博</u><br/>@虫虫游戏助手</dt></dl><dl><dd><img src=\"http://static.ccplay.com.cn/static/common/img/code.png\"/></dd><dt>扫描即可下载<br/>虫虫助手</dt></dl><b class=\"s-triangle\">&diams;</b></div></li><li><a href=\"http://bbs.ccplay.com.cn/thread-59101-1-1.html\"target=\"_blank\"class=\"a-problems\"><span>常见问题</span></a></li><li><a href=\"javascript:;\"class=\"a-top\"id=\"toTop\"><span>返回顶部</span></a></li></ul></div>");
function toTopHide(){if(document.documentElement.scrollTop+document.body.scrollTop>90){document.getElementById("toTop").style.display="block"}else{document.getElementById("toTop").style.display="none"}}$(function(){$(window).scroll(function(){toTopHide();$("#toTop").click(function(){window.scrollTo(0,0);return false})})});




$(function(){
	
/*返回顶部*/
	 $(window).scroll(function(){
        toTopHide();
        $("#toTop").click(function(){
            window.scrollTo(0,0);
            return false;
        });
    });
	$(".li_code").hover(function(){
       $(this).find(".qr-code-box").fadeIn(300).hover(function(){
				$(this).find("img").css({"opacity":"0.1"});
	 		}, function(){
	   			$(this).find("img").css({"opacity":"1"});
			});
	 }, function(){
	   $(this).find(".qr-code-box").fadeOut(300);
	});		
	$(".qr-code-box dl").hover(function(){
       $(this).find("img").css({"opacity":"1"});
	 }, function(){
	   $(this).find("img").css({"opacity":"0.1"});
	});	


//一键安装提示
	$(".browsers_ad_close_gray").on("click", function() {
		$(".cc-down-tip-box").toggle();
	});


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
/*	$(".key").keyup(function(){		
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
	li_btn($(".game-gift-list"),".btn");	
	li_btn($(".review_list"),".r3");	
	li_btn($(".review_list"),".r4");	
	
//首个APP展开	
	function li_hover(eobj,cssClass){
		eobj.hover(function(){
		   $(this).siblings().removeClass(cssClass);
		   $(this).addClass(cssClass);
		});
	};	
	li_hover($(".app-list-right li"),"hover");
	
	$(".app-list-right").find("li:first").addClass("hover");
	



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



//举报 纠错-表单验证
	var report=$(".report-form").Validform({
		showAllError:true,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".Validform_checktip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		}
	});	
	report.addRule([{
		ele:".fbkcontent",datatype:"*"}
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
                page_load('#comment-list', $('#comment-list .page'), 1);
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
		//举报 纠错
		$(".report").click(function(){
			$(".report-box").zxxbox({
				title: "虫虫游戏问题反馈"	,fix: true, bgclose:true
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

	
	
});







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



/*百度分享*/
window._bd_share_config={"common":{"bdSnsKey":{},"bdText":"","bdMini":"2","bdPopupOffsetLeft":"-228","bdPopupOffsetTop":"-133","bdMiniList":["mshare","qzone","tsina","weixin","tqq","sqq"],"bdPic":"","bdStyle":"0","bdSize":"16"},"share":{}};with(document)0[(getElementsByTagName('head')[0]||body).appendChild(createElement('script')).src='http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion='+~(-new Date()/36e5)];