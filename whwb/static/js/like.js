$(document).ready(function(){
    $("#ilove").hide();
    $("#loveme_btn").click(function(){
	    $("#ilove_btn").removeClass("clck");
	    $("#loveme_btn").addClass("clck");		
	    $("#loveme").show().next().hide();
		
	})
	$("#ilove_btn").click(function(){
	    $("#loveme_btn").removeClass("clck");
		$("#ilove_btn").addClass("clck");
	    $("#ilove").show().prev().hide();
	})
})