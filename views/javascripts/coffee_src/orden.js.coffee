class Orden
  constructor: (producto_id, nombre, precio) ->
    @id = 0
    @producto_nombre = nombre
    @producto_nombre_original = nombre
    @precio_producto = precio
    @precio_unitario = precio
    @precio_total = precio
    @producto_id = producto_id
    @cantidad = 1
    @llevar = false
    @modificadores_producto = new Array()
    @div = null

  fromJSON: (orden_json) ->
    @id = orden_json.id
    @producto_id = orden_json.producto.id
    @producto_nombre_original = orden_json.producto.nombre
    @producto_nombre = @producto_nombre_original
    @precio_producto = orden_json.producto.precio
    @precio_unitario = @precio_producto
    @llevar = orden_json.llevar
    for orden_modificador_producto in orden_json.modificadores_producto
      modificador_producto = orden_modificador_producto.modificador_producto
      modificador = new Modificador(modificador_producto.id, modificador_producto.modificador.nombre,modificador_producto.costo)
      this.agregaModificador(modificador)
    this.toHtml()
    this.setCantidad(orden_json.cantidad)
    return this

  toJSON: () ->
    {
      id : @id,
      producto_id : @producto_id,
      cantidad: @cantidad,
      llevar: @llevar,
      modificadores_producto: JSON.stringify(@modificador_producto)
    }

  setCantidad: (cantidad)->
    @cantidad = parseInt(cantidad)
    @precio_total = @cantidad * @precio_unitario
    @div.children('.precio_total').html(@precio_total)

  agregaModificador: (modificador) ->
    @modificadores_producto.push(modificador)
    @precio_unitario = @precio_producto
    @producto_nombre = @producto_nombre_original
    for modificador in @modificadores_producto
      @precio_unitario += parseInt(modificador.costo)
      @producto_nombre += " #{modificador.nombre}"
    @precio_total = @precio_unitario

  guardar: (nota_id) ->
    data = jQuery.ajax(
      type: 'POST'
      url: '/notas/'.concat(nota_id).concat('/ordenes/')
      data: { 'orden' : JSON.stringify(this) }
      async: false
      success: (data) ->
        return data
      error: ->
        alert 'Error: No se guardo la orden'
    )
    @id = data.responseText

  toHtml: ->
    @div = $('<div class="orden">').data('orden',this)
    @div.append('<input type="checkbox" class="input checkbox llevar" name="llevar"/>')
    @div.append($('<select class="cantidad">').append([1,2,3,4,5,6,7,8,9,10].map((i) -> return "<option>#{i}</option>").join("")).val(@cantidad))
    @div.append("<span class='producto_nombre'>#{@producto_nombre}</span><span class='precio_unitario'>#{@precio_unitario}</span><span class='precio_total'>#{@precio_total}</span>")
    @div.append($('<a href="#" class="borrar">').html("Borrar"));
    @div

  update: (nota_id)->
    jQuery.ajax(
      type: 'PUT'
      url: "/notas/#{nota_id}/ordenes/#{@id}"
      data: { 'cantidad' : @cantidad}
      error: ->
        alert 'Error: No se guardo la nota'
    )