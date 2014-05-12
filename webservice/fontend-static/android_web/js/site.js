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

//合集 巨作
jQuery(".roll").slide({ mainCell:"ul",vis:0,scroll:3,prevCell:".prev",nextCell:".next",easing:"easeInQuint",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//详细缩略图
jQuery(".up_box").slide({ mainCell:"ul",vis:0,scroll:2,prevCell:".prev",nextCell:".next",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//合集页
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
    $.zxxbox.remind('<span class="db pb15 f16">请输入您注册的电子邮箱，下一步将发送修改密码链接到该邮箱。</span><input class="pct50 bg-white pl10 bg-white bde pt10 pb10 f16" type="text" placeholder="请输入电子邮箱" id="p-email" datatype="e">', function(){
        //alert("哇哈哈");
    }, {
        title: "找回密码"		,bg: true, fix: true, bgclose:true
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






