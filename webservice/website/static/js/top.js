$(document).ready(function(){
			var topMain=$("#header").height()+0//是头部的高度加头部与nav导航之间的距离。
			var nav=$(".headbg");
			$(window).scroll(function(){
				if ($(window).scrollTop()>topMain){//如果滚动条顶部的距离大于topMain则就nav导航就添加类.nav_scroll，否则就移除。
					nav.addClass("nav_scroll");
				}
				else
				{
					nav.removeClass("nav_scroll");
				}
			});
 
	})
	
	
	