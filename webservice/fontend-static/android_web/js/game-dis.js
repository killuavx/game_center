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
