// JavaScript Document
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
	}else if(width > 1000){
		wobj.attr("id","cc-m");	
	}else{
		wobj.attr("id","cc-s");	
	}
};



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
	$(".logo .rel").hover(function(){
		$(this).find(".home").fadeIn(200);
	},function(){
		$(this).find(".home").fadeOut(200);
	});
	
	$(".box_btn,.collection_box").hover(function(){
		$(this).find(".a_btn").fadeIn(100);
	},function(){
		$(this).find(".a_btn").fadeOut(100);
	});
	
	$(".sort").hover(function(){
		$(this).find(".sort-menu").fadeIn(100);
	},function(){
		$(this).find(".sort-menu").fadeOut(100);
	});
	
	
	
	$(".btn-s-box dl,.app-list-min,.maste_lsit").hover(function(){
		$(this).find(".btn-s").show();
	},function(){
		$(this).find(".btn-s").hide();
	});
	
	
	$(".maste_lsit").hover(function(){
		   $(".maste_lsit").removeClass("hover");
		   $(this).addClass("hover");
	});
	
	$(".game .app-list-right li").hover(function(){
		   $(".game .app-list-right li").removeClass("hover");
		   $(this).addClass("hover");
	});
	
	$(".soft .app-list-right li").hover(function(){
		   $(".soft .app-list-right li").removeClass("hover");
		   $(this).addClass("hover");
	});
	
	$(".left-top-list .app-list-right li").hover(function(){
		   $(".left-top-list .app-list-right li").removeClass("hover");
		   $(this).addClass("hover");
	});
	
	$(".n-top-app-list li").hover(function(){
		   $(".n-top-app-list li").removeClass("hover");
		   $(this).addClass("hover");
	});

	
	$(".app-list-right").find("li:first").addClass("hover");
	$(".hot-bbs .hot-bbs-list").find("li:first").addClass("first");
	
	
	
	$(".mm-pic-list .mm").hover(function() { // Mouse over
		$(this)
			.stop().fadeTo(500, 1)
			.siblings().stop().fadeTo(500, 0.2);		
	}, function() { // Mouse out
		$(this)
			.stop().fadeTo(500, 1)
			.siblings().stop().fadeTo(500, 1);
	});



//基本资料
	var info=$(".user-info-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:false,
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

//联络信息
	var contact=$(".user-contact-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:false,
		//ajaxPost:true
	});	
	contact.addRule([{
		ele:".w200:eq(4)",datatype:"*"}
	]);


//修改密码
	var password=$(".user-password-form").Validform({
		tiptype:3,
		label:"label",
		showAllError:false,	
		//ajaxPost:true
	});	
	password.addRule([{
		ele:".w200",datatype:"*6-16"},{
		ele:".w200:eq(2)",datatype:"*6-16",recheck:"new_password"}
	]);
	
//注册表单
	var reg=$(".reg-form").Validform({
		showAllError:false,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".login-tip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		},
		//ajaxPost:true
	});

//登录表单
	var reg=$(".login-form").Validform({
		showAllError:false,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".login-tip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		},
		//ajaxPost:true
	});
	
	

	

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
jQuery(".roll").slide({ mainCell:"ul",vis:0,scroll:3,prevCell:".prev",nextCell:".next",easing:"easeInQuint",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//详细缩略图
jQuery(".up_box").slide({ mainCell:"ul",vis:0,scroll:2,prevCell:".prev",nextCell:".next",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//专题页
jQuery(".collection_box").slide({ mainCell:".inner-box",vis:0,scroll:1,prevCell:".prev",nextCell:".next",easing:"easeInQuint",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});






//initiating jQuery
$(".pin-box").pin({
      containerSelector: ".width"
});

$(".nav").pin()




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
                this.style.color = '#ddd';    
            }
        };
        
        //样式初始化
        if (element.value === "") {
            element.value = placeholder;
            element.style.color = '#ddd';    
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




$(function(){	
		//登录
		$(".open-login").click(function(){
			$(".login-box").zxxbox({
				title: "会员登录"	,fix: true, bgclose:true
				});
		});
		//注册
		$(".open-reg").click(function(){
			$(".reg-box").zxxbox({
				title: "用户注册"	 ,fix: true, bgclose:true
				});
		});
});











$(function() { 	
	
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
//<div class="p20 f20 white"><i class="icon-minus-sign mr10 f28"></i><span class="dib rel">禁止！~</span></div>



	
	//询问

	$("#box_remind").click(function(){
    $.zxxbox.remind('<span class="f16 tc">文字内字文字内容区域文字内容区域文字内容区域文<br/>字内容区域文字内容区域文字内容区域文字内容区域文字内容区域，<br/>支持HTML 支持HTML 支持HTML</span>', function(){
        //alert("哇哈哈");
    }, {
        title: "询问标题"		,delay: 2000,bg: true, fix: true, bgclose:true
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
	

	
})
//弹出框提示 结束






