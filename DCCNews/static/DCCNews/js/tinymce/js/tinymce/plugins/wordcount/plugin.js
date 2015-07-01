/**
 * plugin.js
 *
 * Released under LGPL License.
 * Copyright (c) 1999-2015 Ephox Corp. All rights reserved
 *
 * License: http://www.tinymce.com/license
 * Contributing: http://www.tinymce.com/contributing
 */

/*global tinymce:true */

tinymce.PluginManager.add('wordcount', function(editor) {
	var self = this, countre, cleanre;

	// Included most unicode blocks see: http://en.wikipedia.org/wiki/Unicode_block
	// Latin-1_Supplement letters, a-z, u2019 == &rsquo;
	countre = editor.getParam('wordcount_countregex', /[\w\u2019\x27\-\u00C0-\u1FFF]+/g);
	cleanre = editor.getParam('wordcount_cleanregex', /[0-9.(),;:!?%#$?\x27\x22_+=\\\/\-]*/g);

	function update(e) {
		editor.theme.panel.find('#wordcount').text(['Caracteres faltantes: {0}', self.getCount(e)]);
	}

	editor.on('init', function() {
		var statusbar = editor.theme.panel && editor.theme.panel.find('#statusbar')[0];

		if (statusbar) {
			window.setTimeout(function() {
				statusbar.insert({
					type: 'label',
					name: 'wordcount',
					text: ['Caracteres faltantes: {0}', self.getCount()],
					classes: 'wordcount',
					disabled: editor.settings.readonly
				}, 0);

				editor.on('setcontent beforeaddundo', update);
				editor.on('keydown', function(e){
					//editor.save();
//					if(e.keyCode == 8 || e.keyCode == 46){
//						editor.getBody().setAttribute('contenteditable', true);
//						editor.undoManager.undo();
//					}
				});
				editor.on('input', function() {
					editor.undoManager.add();
					update();
				});
//				editor.on('undo', function(){
//					editor.getBody().setAttribute('contenteditable', true);
//				});

			}, 0);
		}
	});

	self.getCount = function() {
		var maxLength =
			{"id_body" : 1000 ,
			 "id_title" : 100,
			 "id_subhead" : 100,
			 "id_exhibitor" : 100,
			 "place" : 100
			};
		console.log("init");
		var tx = editor.getContent();
		var element = editor.getElement();
		//var max = element.maxLength;
		var max = maxLength[element.id];
		//var range = editor.selection.getRng();
		//console.log(range);
		var tc = 0;
		tx = tx.replace(new RegExp('(</?(p|strong|em)>)', 'g'), '');
		tx = tx.replace(new RegExp('<p style="text-align: (right|center|left|justify);">', 'g'), '');
		tx = tx.replace(new RegExp('(&nbsp;)', 'g'), ' ');
		tc = tx.length;
		if(max - tc < 1){
			editor.getBody().setAttribute('contenteditable', false);
		}else{
			editor.getBody().setAttribute('contenteditable', true);
		}
		return max - tc;
	};

});
/*
Tengo algo, espero que les guste porque es lo mejor que se me ocurrio, todo esto en el contexto de detener al usuario cuando usa mas caracteres de lo permitido, la idea es que cuando usa mas caracteres de lo permitido el editor se bloquea y no puede escribir ni borrar, lo que debe hacer es deshacer ( con el boton deshacer ) el ultimo cambio y puede continuar editando....
esto es lo mejor que se me a ocurrido, tal ves pueda hacer que le permita borrar un segmento seleccionado de la cadena ( lo vere mañana)...
despues de unas ediciones me di cuenta que permite remplazar un segmento por un caracter lo cual funciona....
pero por lo menos el enrequesimiento de texto funciona (se guarda, previsulizar nunca me funciona... )
TODO:
BUGS:
- dado que el conteo de caracteres es sin tag mientras se ve, pero el con tags en los formularios, exite la posibilidad que el usuario vea que le quedan caracteres pero por los tag le de un error de exceso de caracteres, lo estoy viendo ahora
- -posible solucion, mover el maximo de caracteres al inicializar el editor, en ves del formulario
- - desabilitar la revision del formulario

- El borrador no guarda.
-- posible sol: cada ves que se cambie el editor pasar el texto al fondo?

posible bug:
- la busqueda no funciona porque difiere lo buscado con el tag
-- sol; buscar palabra por palabra, en ves del texto entero...
*/