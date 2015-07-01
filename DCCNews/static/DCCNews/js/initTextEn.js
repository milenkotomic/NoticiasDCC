		tinymce.init({
    		selector: "input#id_title",
    		menubar: false,
    		toolbar: [ "styleselect | bold italic underline | alignleft aligncenter alignright alignjustify | undo redo" ],
			plugins: "wordcount",
			style_formats: [
			                {title: 'Titulo', inline: 'b'},
			                {title: "Contenido", icon: "alignjustify", format: "alignjustify"}

			               ]       
	 	});

		tinymce.init({
    		selector: "input#id_subhead",
    		menubar: false,
    		toolbar: [ "styleselect | bold italic underline | alignleft aligncenter alignright alignjustify | undo redo" ],
			plugins: "wordcount",
			style_formats: [
			                {title: 'Titulo', inline: 'b'},
			                {title: "Contenido", icon: "alignjustify", format: "alignjustify"}

			               ]       
	 	});
		tinymce.init({
    		selector: "textarea",
    		menubar: false,
    		toolbar: [ "styleselect | bold italic underline | alignleft aligncenter alignright alignjustify | undo redo" ],
			plugins: "wordcount",
			style_formats: [
			                {title: 'Titulo', inline: 'b'},
			                {title: "Contenido", icon: "alignjustify", format: "alignjustify"}

			               ]       
	 	});
