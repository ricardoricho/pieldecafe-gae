jQuery(document).ready( ->
  jQuery.ajax({
    type: 'GET'
    url: '/notas'
    data: { 'abierta' : true }
    dataType: 'json'
    success: (notas) ->
      $(notas).each( (i, nota_json) ->
        nota = new Nota(nota_json.nombre)
        $("#notas").append(nota.fromJSON(nota_json))
      )
      $("#notas .nota:first").addClass("active")
  })

  $("a[data-id]").click( ->
    nota_html = $(".nota.active")
    if nota_html.length  == 0
      nota_html = nuevaNota()
    nota = nota_html.data('nota')
    orden = new Orden($(this).data('id'), $(this).data('nombre'), parseFloat($(this).data('precio')) )
    jQuery.ajax({
      type: 'GET'
      url: '/productos/'.concat($(this).data('id')).concat('/modificadores')
      dataType: 'json'
      success: (data) ->
        if data != null and data.length > 0
          dialogo(nota, data, orden)
        else
          nota.agregaOrden(orden)
          orden.guardar(nota.id)
          nota.update()
    })
  )

  dialogo = (nota_activa, data, orden) ->
    cuerpo = $("#modificadores .modal-body").data('orden', orden).empty().html('')
    modificadores = {}
    for modificador_producto in data
      if(modificadores[modificador_producto.modificador.tipo.nombre])
        modificadores[modificador_producto.modificador.tipo.nombre]['modificador']
        .push(
          'id': modificador_producto.id
          'nombre': modificador_producto.modificador.nombre
          'costo': modificador_producto.costo
          'default': modificador_producto.default
          'excluyente' : modificador_producto.modificador.tipo.excluyente
        )
      else
        modificadores[modificador_producto.modificador.tipo.nombre] =
            'modificador' : [
              'id': modificador_producto.id
              'nombre' : modificador_producto.modificador.nombre
              'costo' : modificador_producto.costo
              'default' : modificador_producto.default
              'excluyente' : modificador_producto.modificador.tipo.excluyente
            ]
    contenido = ""
    for nombre_categoria, categoria of modificadores
      contenido = contenido.concat("<h4>#{nombre_categoria}</h4>")
      for modificador in categoria.modificador
        if modificador.excluyente
          tipo = "radio"
        else
          tipo = "checkbox"
        contenido = contenido.concat("<label class='#{tipo}'><input type='#{tipo}'")
        .concat(" name='#{nombre_categoria}' data-id='#{modificador.id}' data-costo='#{modificador.costo}'")
        .concat(" data-nombre='#{modificador.nombre}'/> #{modificador.nombre} </label>")
    cuerpo.append(contenido)
    $("#modificadores").modal('show')

  $(document).on('click','#modificadores .modal-footer a', () ->
    orden = $("#modificadores .modal-body").data('orden')
    $("#modificadores .modal-body :checked").each( ->
      modificador = new Modificador($(this).data('id'), $(this).data('nombre'), parseFloat($(this).data('costo')))
      orden.agregaModificador(modificador)
    )
    $("#modificadores").modal('hide')
    nota = $(".nota.active").data('nota')
    orden.guardar(nota.id)
    nota.agregaOrden(orden)
    nota.update()
  )

  $("#nota_nueva").click( ->
    nuevaNota()
  )

  nuevaNota =  ->
    nota_nueva = jQuery.ajax(
      type: 'GET'
      url: '/notas/new'
      async: false
      success: (data) ->
        return data
      error: ->
        alert 'Error: Falló crear nota'
    )
    data = JSON.parse(nota_nueva.responseText)
    nota = new Nota()
    nota.id = data.id
    nota.nombre = "Nota_#{nota.id}"
    $("#notas").append( nota.toHtml() )
    $(".nota").each( ->
      $(this).removeClass("active")
    )
    nota.div.addClass("active")
    return nota.div


  $(document).on('click', '.nota', ->
    $(".nota").each( ->
      $(this).removeClass("active")
    )
    $(this).addClass("active")
  )

  $(document).on('change','.cantidad', ->
    orden = $(this).parent('.orden').data('orden')
    nota = $(".nota.active").data('nota')
    orden.setCantidad($(this).val())
    orden.update(nota.id)
    nota.calculaTotal()
    nota.update()
  )

  $(document).on('click', '.borrar', ->
    orden = $(this).parent('.orden').data('orden')
    nota = orden.div.parents('.nota').data('nota')
    jQuery.ajax(
      url: "/notas/#{nota.id}/ordenes/#{orden.id}"
      type: "DELETE"
      success: (data) ->
				nota.borrarOrden(orden)
        orden.div.empty().remove()
    )
  )

  $(document).on('click','.cerrar', ->
    nota = $(this).parents('.nota').data('nota')
    jQuery.ajax(
      url: "/notas/#{nota.id}"
      type: 'PUT'
      data: {	'abierta' : false }
      success: (data) ->
        nota.div.empty().remove()
    )
  )

  $(document).on('click','.imprimir', ->
    nota = $(this).parents('.nota').data('nota')
    nota.imprime()
  )

)
