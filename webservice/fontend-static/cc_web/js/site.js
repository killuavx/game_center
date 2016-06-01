/*焦点图*/
$(".focusBox").slide({ titCell:".num-box ul" , mainCell:".focusBox_pic ul" , autoPlay:true,  autoPage:true,startFun:function(i){		 
$(".focusBox .txt li").eq(i).animate({"left":0}).siblings().animate({"left":-1000});}});
/*今日头条*/
$(".txtScroll").slide({mainCell:"ul",autoPage:true,effect:"topLoop",easing:"easeInQuint",autoPlay:true});
/*产品*/
$(".productBox").slide({ titCell:".num-box ul" , mainCell:".productBox_pic ul" , autoPlay:true, effect:"fold", autoPage:true });