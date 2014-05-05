

jQuery(".focusBox").slide({ titCell:".num li", mainCell:".pic", autoPlay:"true",prevCell:".prev",nextCell:".next",
startFun:function(i){		 
jQuery(".focusBox .txt li").eq(i).animate({"left":0}).siblings().animate({"left":-1000});}
});


jQuery(".productBox").slide({ titCell:".num li", mainCell:".pic",effect:"leftLoop", autoPlay:"true", prevCell:".prev",nextCell:".next"});


jQuery(".txtScroll").slide({mainCell:"ul",autoPage:true,effect:"topLoop",easing:"easeInQuint",autoPlay:true});