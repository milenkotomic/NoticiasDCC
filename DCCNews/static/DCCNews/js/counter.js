// pasa por todos los atributos de los formularios con id formID,
// y le agrega los contadores de caracteres, si estos son tipos texto
// textarea y su tamaño maximo es menor a 10000
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
//	$("input#id_new_tag").maxlength({
//		alwaysShow: true,
//		showCharsTyped: false,
//     showMaxLength: false
//	});
//	$("input#id_exhibitor").maxlength({
//		alwaysShow: true,
//		showCharsTyped: false,
//     showMaxLength: false
//	});
//	$("input#id_place").maxlength({
//		alwaysShow: true,
//		showCharsTyped: false,
//     showMaxLength: false
//	});
});
