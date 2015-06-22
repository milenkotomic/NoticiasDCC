$(document).ready(function(){
 		$("form#formID input[type=text]").each(function(){
		 	var input = $(this);
		 	//console.log(input);
		 	if(input.attr('maxLength')<10000){
		 		input.maxlength({
          		alwaysShow: true,
          		showCharsTyped: false,
 		        showMaxLength: false
      		});
		 	}
		});
		$("form#formID textarea").each(function(){
		 	var input = $(this);
		 	//console.log(input);
		 	if(input.attr('maxLength')<10000){
		 		input.maxlength({
          		alwaysShow: true,
          		showCharsTyped: false,
 		        showMaxLength: false
      		});
		 	}
		});
});
