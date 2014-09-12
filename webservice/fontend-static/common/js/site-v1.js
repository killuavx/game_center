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
		
		/*if($(window).scrollTop()<=0) {
			_html.attr("ID","");
		}else{
			_html.attr("ID","fixed-head");
		}*/
		
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

//一键安装提示
	$(".browsers_ad_close_gray").on("click", function() {
		$(".cc-down-tip-box").toggle();
	});
	
	//登录后
	jQuery(".user-switch").slide({ type:"menu", titCell:"li", targetCell:"dl", delayTime:300, triggerTime:0,returnDefault:true  });
	//.change-password
	//.log-out	
	
	$(".change-password").click(function(){
		$.zxxbox($(".change-password-box"), {
        title: "修改密码"	, fix: true
        });
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
	
	
	
	
});

