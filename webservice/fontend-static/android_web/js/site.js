/*
 * app详情图片事件绑定
*/

var imgloadCount = 0;
function bindAppDetailCoverEv(vis_count){

	var e = $(".up_pic img");
	var imageCount = e.size();
	
	if(imgloadCount == 0){
	
		e.each(function(){
			if(this.complete){
				imgloadCount++
			}
		});
		
		if(imgloadCount == imageCount){
			jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		}else{
			e.load(function(){
				imgloadCount++;
				if(imgloadCount == imageCount){
					jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
				}
			});
		}
	}else{
		jQuery(".up_box").slide({ mainCell:"ul",vis:1,scroll:1,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		
	}	
}

function resize(){
	var width = $(window).width();
	var wobj = $("body");
	if(width > 1250){
		wobj.attr("id","cc-l");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:5,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:4,scroll:4,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(4);
	}else if(width > 990){
		wobj.attr("id","cc-m");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:4,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:3,scroll:3,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(3);

	}else{
		wobj.attr("id","cc-s");	

		/*巨作*/
		jQuery(".roll").slide({ mainCell:"ul",vis:3,scroll:2,prevCell:".prev",nextCell:".next",autoPage:true,effect:"leftLoop",autoPlay:false});
		/*详细缩略图*/
		//jQuery(".up_box").slide({ mainCell:"ul",vis:2,scroll:2,prevCell:".prev",nextCell:".next",effect:"left",pnLoop:false,autoPage:true,easing:"easeOutCubic"});
		bindAppDetailCoverEv(2);

	}
};



$(function(){
	
	//举报 纠错-表单验证
	var report=$(".report-form").Validform({
		showAllError:true,	
		tiptype:function(msg,o,cssctl){
			var objtip=$(".Validform_checktip");
			cssctl(objtip,o.type);
			objtip.text(msg);
		}
	});	
	report.addRule([{
		ele:".fbkcontent",datatype:"*"}
	]);
	
	
	//举报 纠错
		$(".report").click(function(){
			$(".report-box").zxxbox({
				title: "虫虫游戏问题反馈"	,fix: true, bgclose:true
				});
		});
	
	
	
	//评论
    var comment_tips = $('#comments .comment-tip');
    var review=$(".comment-form").Validform({
        showAllError:true,
        tiptype:function(msg,o,cssctl){
            var objtip=$("");
            cssctl(comment_tips,o.type);
            objtip.text(msg);
        },
        ajaxPost:true,
        callback: function(data){
            if( data.code == 0 )
            {
                comment_tips.html('');
                page_load('#comment-list', $('#comment-list .page'), 1);
                $('.comment-form textarea[name=comment]').val('');
                $('.comment-form input[name=rating_output]').val('');
                $('#rating_on').attr('style', '');
                alert(data.msg);
            }
            else
            {
                var msgs = [];
                for(k in data.errors)
                {
                    msgs.push(data.errors[k].join(','));
                }
                var _msg = data.msg + " " + msgs.join(", ")
                comment_tips.html(_msg);
            }
            return false;
        }
    });
	review.addRule([{
		ele:".comment-box",datatype:"*1-300"}
	]);	
	
	
	
	
});


//评分
$(document).ready(function(){
	$('#rating_btns li').hover(function(){	
			$rating = $(this).text();
			$('#rating_on').css('width', rateWidth($rating));
	},function(){
		 $rating = $('#rating').text();
		if($rating == ""){		
			 $('#rating_on').css('width', "0px");
		 }
		 else{
			 $('#rating_on').css('width', rateWidth($rating));	
		 }
	});
	$('#rating_btns li').click(function(){
		$rating = $(this).text();			
		$('#rating').text($rating+'分');
		$('#rating_output').val($rating);
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
$(document).ready(function(){
    function page_load(load_box, dom, p){
        var _load_box = $(load_box);
        var url = $(dom).attr('data-url');
        if( !url ){
            return false
        }
        $.ajax({
            type:'get',
            url:url,
            data:{
                page:p
            },
            dataType:'html',
            success:function(data){
                _load_box.html(data);
            }
        });
        return false;
    }
    window.page_load = page_load;
});
