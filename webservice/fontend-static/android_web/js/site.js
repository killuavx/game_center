jQuery(".slideGroup").slide({titCell:".parHd li",mainCell:".parBd"});

$(function(){
	function dd_a(eobj,cssClass){
		eobj.click(function(){		  
		   $(this).find(cssClass).addClass();
		},function(){
			 $(this).find(cssClass).removeClass();
		});
	};	
	dd_a($(".app-list-min,.app-list-xl,.maste_lsit"),".btn-s");
});

