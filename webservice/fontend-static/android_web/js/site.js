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
	
});