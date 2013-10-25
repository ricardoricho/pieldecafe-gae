class Nota
  constructor: (@nombre) ->
    @id = 0
    @total = 0
    @div = null
    @ordenes = new Array()

  fromJSON: (nota_json) ->
    @id = nota_json.id
    @total = nota_json.total
    @nombre = nota_json.nombre
    @total = 0
    this.toHtml()
    for orden_json in nota_json.ordenes
      orden = new Orden()
      orden = orden.fromJSON(orden_json)
      @ordenes.push(orden)
      @div.children('.ordenes').append(orden.toHtml())
    this.calculaTotal()
    @div

  calculaTotal: ->
    suma = 0
    for orden in @ordenes
      suma += orden.precio_total
    @total = suma
    @div.children('.total').children('.resultado').html(@total)

  guardar: () ->
    jQuery.ajax({
      type: 'POST'
      url: '/notas'
      data: { 'nota' : JSON.stringify(this)}
      success: (data) ->
      error: ->
        alert('Error al guardar nota')
    })

  toHtml: () ->
    @div = $('<div class="nota">').data('nota', this)
    @div.html('<span class="nombre">'+ @nombre + '</span>'
      .concat('<div class="ordenes"></div>')
      .concat('<div class="total">Total: <span class="resultado">')
      .concat( @total).concat('</span>')
      .concat('<a href="#" class="cerrar">Cerrar<a href="#" class="imprimir">')
      .concat('Imprimir'))
    @div

  agregaOrden: (orden) ->
    @ordenes.push(orden)
    @div.children('.ordenes').append(orden.toHtml())
    this.calculaTotal()

  borrarOrden: (orden) ->
    for orden_nota in @ordenes
      if(orden.id == orden_nota.id)
        @ordenes.splice(_i, 1)
        return @calculaTotal()

  imprime: ->
    doc = "Cant. ".concat(Array(9).join(" "))
    .concat("Producto").concat(Array(9).join(" "))
    .concat("P.U.  P.T.\n")
    d = new Date()
    for orden in @ordenes
      doc = doc.concat(orden.cantidad).concat(Array(4).join(" "))
      .concat(orden.producto_nombre.substring(0,26))
      .concat(Array(26-(orden.producto_nombre.substring(0,26).length)).join(" "))
      .concat(orden.precio_unitario)
      .concat("   ").concat(orden.precio_total).concat("\n")
    doc = doc.concat(Array(41).join("-")).concat("\n")
    .concat("Total:").concat(Array(30).join(" "))
    .concat(@total)
    PielDeCafe.imprimeNota(doc, $("#usuario").text(), "#{d.getDate()}/#{d.getMonth()+1}/#{d.getFullYear()}",d.toTimeString().substring(0,5))

  update: ->
    jQuery.ajax(
      type: 'PUT'
      url: "/notas/#{@id}"
      data: { 'total' : @total}
      success: (data) ->
      error: ->
        alert 'Error: No se guardo la nota'
    )