/*  点击提交按钮检测input里面是否有空格，对于page_two有效，对界面一另写js */
    $(document).ready(function(){
	    $("#submit").click(function(){
		    $("input").each(function(){
			    if($(this).val().indexOf(" ")>=0){
				    $("#submit").attr("disabled",true);
				    $(this).focus(); 
			        return false;				
				}	
			});
			setTimeout(function(){
			    $("#submit").attr("disabled",false)},500)
			pageoneShowAutofocus();
		})

	 });
/* pageoneShowAutofocus()是针对界面一自动聚焦到有空格的input中的 */
	function pageoneShowAutofocus(){
	    var qqspace=$("#qq").val().indexOf(" ");
		var passwordspace=$("#password").val().indexOf(" ");
		if(passwordspace>=0 ){
			$("#page_two").hide().prev().show(); 
			$("#password").focus(); 
		}		
		if(qqspace>=0 ){
			$("#page_two").hide().prev().show(); 
			$("#qq").focus(); 
		}
	}