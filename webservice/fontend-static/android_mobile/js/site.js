/*隐藏提示*/
$(".tip-close-box").on("click", function() {
	$(".cc-down-tip").toggle();
});

/*下载提示*/
function alertDialogShow(){
	$('#alertDialogId').removeClass('dn');
}
$(".li-down,.li-cancel,.cc-pop-bg").on("click", function() {
	$('#alertDialogId').addClass('dn');
});

//最小高度
var screen_height = $(window).height();
var head_height = $('header').outerHeight(true);  
var foot_height = $('footer').outerHeight(true);
var $body = $('.minheight-page');
if ($body.size()) {
  var bodyMarginTop = $body.css("marginTop").replace('px', '');
  var bodyMarginBottom = $body.css("marginBottom").replace('px', '');  
  var body_height = screen_height - head_height - foot_height - bodyMarginTop - bodyMarginBottom;  
  $body.css('min-height', body_height + 'px');
}

/*菜单*/
$(".go-menu").on("click", function() {
	$(".nav").toggle();
});

//搜索提示
$(".search-input").keyup(function(){		
	var inputvalue = $(".search-input").val();
	if(inputvalue  != ""){
		$('.search-input-submit').show().animate({opacity:"1"},200);
		$('.search-input-cancel').hide().animate({opacity:"0"},200);
	}else if(inputvalue == ""){
		$(".search-input-submit").hide().animate({opacity:"0"},200);
		$(".search-input-cancel").show().animate({opacity:"1"},200);
	};		
});

$(".search-input-cancel,.go-back").click(function(){	
	window.history.go(-1);	
	return false;
});

//查看更多
$(function() { 	
	$(".text_inner").click(function(){
		var hei = $(this).find('div').css("height");
		if ( hei == "42px" )
		{
			$(this).find('div').css({"overflow":"hidden","height":"auto"});
			$(this).find('span').addClass('p-up');
		}
		else
		{
			$(this).find('div').css({"overflow":"hidden","height":"42px"});
			$(this).find('span').removeClass('p-up');
		}		
    });		
})
/*百度统计*/
var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");
document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3Fc9a240c247e29f79e2ee021cd7246eaf' type='text/javascript'%3E%3C/script%3E"));