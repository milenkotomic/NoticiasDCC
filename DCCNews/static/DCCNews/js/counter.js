// pasa por todos los atributos de los formularios con id formID,
// y le agrega los contadores de caracteres, si estos son tipos texto
// textarea
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
