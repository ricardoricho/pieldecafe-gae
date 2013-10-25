jQuery(document).ready(function(){	
	formaModificador = function(producto_id){
		var forma = $('<div id="formaNuevoModificador" class="form-inline">');
		var tipos_modificador = $('<select name="tipoModificador" class="tiposModificador input-small span3">')
		forma.append('<label for="tipoModificador"> Tipo: </label>');
		jQuery.ajax({
			type : 'GET',
			url : '/tipos_modificador',
			contentType : 'application/json',
			dataType: 'json',
			success: function(data){
				tipos_modificador.append('<option></option>');
				for (tipo in data) {
					tipos_modificador.append('<option value='.concat(data[tipo].id)
											 .concat('>').concat(data[tipo].nombre).concat('</option>'));
				}
			}
		});
		forma.append(tipos_modificador);
		forma.append('Modificador: <select class="modificadores input-small span3" disabled="disabled"></select>');
		forma.append('Costo: <input class="valor input-small" type="text" name="valor" disabled="disabled" />');
		forma.append('<a class="submitModificador btn btn-danger" data-id='
					 .concat(producto_id).concat('>Agregar</a>'));
		return forma;
	}
	$(".agregaModificador").click(function(){
		$(this).parent().siblings('.nuevoModificador').html(formaModificador($(this).data('id')));
		return false;
	});
	$(document).on('change','.tiposModificador', function(){
		tiposMod = $(this);
		modificadores = tiposMod.siblings('.modificadores');
		if(tiposMod.val() !== ''){
			jQuery.ajax({
				type : 'GET',
				url : '/tipos_modificador/'.concat($(this).val()).concat('/modificadores'),
				contentType : 'application/json',
				dataType: 'json',
				success: function(data){
					modificadores.removeAttr('disabled');
					modificadores.html('<option></option>');
					for (modificador in data) {
						modificadores.append('<option value='.concat(data[modificador].id).concat('>')
											 .concat(data[modificador].nombre)
											 .concat('</option>'));
					}
				}
			});
		}else{
			modificadores.val('').attr('disabled','disabled');
		}
	});
	$(document).on('change','.modificadores', function(){
		modificadores = $(this);
		valor = $(this).siblings('.valor');
		if($(this).val() !== ''){
			valor.removeAttr('disabled');			
		}else{
			valor.val('').attr('disabled','disabled');
		}
	});
	$(document).on('click','.submitModificador', function(){
		tiposMod = $(this).siblings('.tiposModificadores');
		modificadores = $(this).siblings('.modificadores');
		valor = $(this).siblings('.valor');
		liga = $(this);
		if(tiposMod.val() !== '' && modificadores.val() !== ''
		   && valor.val() !== ''){
			console.log('enviando..');
			jQuery.ajax({
				type : 'POST',
				url : '/productos/'.concat($(this).data('id')).concat('/modificadores'),
				data : { 
					modificador_id : modificadores.val(),
					costo: valor.val()
				},
				dataType: 'json',
				success: function(data){
					liga.parents('.nuevoModificador')
						.siblings('.listaModificadores')
						.append('<tr><td>'.concat(modificadores.children("option:selected").text())
								.concat('</td><td>')
								.concat(data.costo).concat('</td><td>')
								.concat(data.producto.precio + data.costo)
								.concat('</td>'));
				}
			});
		}
	});

	$(document).on('click','.borrarModificadorProducto', function(){
		boton = $(this)
		jQuery.ajax({
			type : 'DELETE',
			url : '/productos/'.concat(boton.data('producto_id')).concat('/modificadores/').concat(boton.data('modificador_producto_id')),
			dataType: 'json',
			success: function(data){
				boton.parents('tr').empty().remove();
			}
		});
		return false;
	});

});
