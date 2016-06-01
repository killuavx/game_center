//浏览器宽度自适应
$(document).ready(function(e) {
  
	  //最小高度
	  var screen_height = $(window).height();
	  var $body = $('.minheight-page');
	  if ($body.size()) { 
		$body.css('min-height', screen_height/2 + 'px');
	  }

});
