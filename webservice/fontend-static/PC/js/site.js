//app install
$(".focus").slide({ titCell:".num ul" , mainCell:".banner_ul" , autoPlay:true, delayTime:700 , autoPage:true });

jQuery(".roll").slide({ mainCell:"ul",vis:4,scroll:1,prevCell:".prev",easing:"easeInQuint",nextCell:".next",effect:"leftLoop", autoPage:true});

jQuery(".collection_box").slide({ mainCell:"ul",vis:5,scroll:2,prevCell:".prev",nextCell:".next",easing:"easeInQuint",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

//jQuery(".up_box").slide({ mainCell:"ul",vis:2,scroll:1,prevCell:".prev",nextCell:".next",effect:"leftLoop",pnLoop:false, autoPage:true,easing:"easeOutCubic"});

jQuery(".box-tab").slide({ titCell:".title_box li", mainCell:".list", targetCell:".tab-more a", effect:"fold",titOnClassName:"hover",});	

bindAppDetailCoverEv()
function bindAppDetailCoverEv(){
	var e = $(".up_pic img");
	var imageCount = e.size();
	var boxWidth = $(".up_pic ").width();
	var totalImageWidth = 0;
	var vis_count = 0;
	var imgloadCount = 0;

	e.each(function(){
		if(this.complete){
			imgloadCount++;
			totalImageWidth += $(this).width();
		}
	});

	if(imgloadCount == imageCount){
		vis_count = boxWidth/(totalImageWidth / imageCount);
		jQuery(".up_box").slide({ mainCell:"ul",vis:vis_count,scroll:vis_count,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
	}else{
		e.load(function(){
			imgloadCount++;
			totalImageWidth += $(this).width();
			if(imgloadCount == imageCount){
				vis_count = boxWidth/(totalImageWidth / imageCount);
				jQuery(".up_box").slide({ mainCell:"ul",vis:vis_count,scroll:vis_count,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
			}
		});
	}
	
}



$(function(){

	$(".refresh").click(function(){
		window.history.go(0);
	});
	
	$(".pgup").click(function(){	
		window.history.go(-1);	
		return false;
	});
	
	$(".pgdn").click(function(){
		window.history.go(1);
		return false;
	});
	
	
	$(".left_list li,.collection_box li,.maste_lsit").hover(function(){
		$(this).find(".btn").fadeIn(100);
		
	},function(){
		$(this).find(".btn").fadeOut(100);
	});
	
	$("li").hover(function(){
		$(this).find(".pop_menu").fadeIn(100);
		
	},function(){
		$(this).find(".pop_menu").fadeOut(100);
	});
	
	$(".home_game_right .list li").hover(function(){
		   $(".home_game_right .list li").removeClass("hover");
		   $(this).addClass("hover");
	});	
	$(".home_soft_right .list li").hover(function(){
		   $(".home_soft_right .list li").removeClass("hover");
		   $(this).addClass("hover");
	});	
	$(".right_list ul").find("li:first").addClass("hover");
	
	
	$(".roll,.focus_left,.collection_box").hover(function(){
		$(this).find(".unslider-arrow").fadeIn(300);		
	},function(){
		$(this).find(".unslider-arrow").fadeOut(300);
	});
	
});




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
