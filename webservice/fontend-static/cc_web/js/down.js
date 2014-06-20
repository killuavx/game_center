/*var animate=function(){
	var topsize=$(window).scrollTop();
	if(topsize>=300){
		$(".d-1 img").addClass("animate")
		}
	if(topsize>=800){
		$(".d-2 img").addClass("animate")
		}
	if(topsize>=820){
		_value=3;
		$(".d-3 img").addClass("animate")
		}
	}
$(window).bind("scroll resize",animate);*/
jQuery(".banner").slide({ titCell:".btn-box a.db",mainCell:".text-box",targetCell:".text-p p", autoPlay:true});