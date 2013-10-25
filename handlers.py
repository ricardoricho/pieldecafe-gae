# -*- coding: utf-8 -*-
import webapp2
import cgi
import logging
import datetime

from webapp2_extras import json
from google.appengine.api import users
from config import jinja_enviroment
from models import *


class MainHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)

    def render_html(self, template, template_values):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        html_template = jinja_enviroment.get_template(template)
        user = users.get_current_user()
        template_values['nombre'] = user.nickname()
        template_values['url_logout'] = users.create_logout_url("/")
        self.response.out.write(html_template.render(template_values))

    def render_json(self, objeto):
        rjson = json.encode(objeto)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(rjson)

    def request_format(self):
        accept_types = self.request.headers['Accept'].split(',')
        return (lambda x: {
                'text/html': {'html': self.render_html},
                'application/json': {'json': self.render_json},
                'application/xml': {'xml': self.render_html}
                }.get(x,'html'))(accept_types[0])

    def respond_with(self, action, parametros):
        if (isinstance(parametros, tuple)):
            action(*parametros)
        else:
            action(parametros)

    def respond_to(self,*args):
        formato = self.request_format()
        for action in args :
            if formato.keys()[0] in action :
                self.respond_with(formato[formato.keys()[0]], action[formato.keys()[0]])


    def get(self):
        user = users.get_current_user()
        if user:
            template_values = {
                'bebidas_calientes' : Producto.gql("WHERE categoria = :1 ORDER BY nombre", 'Bebidas Calientes'),
                'bebidas_frias' : Producto.gql("WHERE categoria = :1 ORDER BY nombre", 'Bebidas Frias'),
                'alimentos' : Producto.gql("WHERE categoria = :1 ORDER BY nombre", 'Alimentos'),
            }
            self.render_html('index.html', template_values)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ProductosHandler(MainHandler):
    # index
    def get(self):
        bebidas_calientes = Producto.gql("WHERE categoria = :1", 'Bebidas Calientes')
        bebidas_frias = Producto.gql("WHERE categoria = :1", 'Bebidas Frias')
        alimentos = Producto.gql("WHERE categoria = :1", 'Alimentos')
        template_values = {
            'bebidas_calientes' : bebidas_calientes,
            'bebidas_frias' : bebidas_frias,
            'alimentos' : alimentos,
        }
        self.render_html('productos/index.html', template_values)

    #show
    def show(self,producto_key):
        producto = Producto.get(producto_key)
        template_values = { 'producto': producto }
        self.render_html('productos/show.html', template_values)

    #new
    def new(self):
        producto = Producto()
        template_values = {
            'producto' : producto,
            }
        self.render_html('productos/new.html', template_values)

    #create
    def post(self):
        producto = Producto()
        producto.nombre = cgi.escape(self.request.get('nombre'))
        producto.precio = float(cgi.escape(self.request.get('precio')))
        producto.categoria = self.request.get('categoria')
        producto.put()
        self.redirect('/productos')

    #edit
    def edit(self, producto_id):
        producto = Producto.get_by_id(long(producto_id))
        if producto :
            template_values = { 'producto' : producto }
            self.render_html('productos/edit.html', template_values)

    #update
    def put(self, producto_id):
        producto = Producto.get_by_id(long(producto_id))
        producto.nombre = cgi.escape(self.request.get('nombre'))
        producto.precio = float(cgi.escape(self.request.get('precio')))
        producto.categoria = self.request.get('categoria')
        producto.put()
        self.redirect('/productos')

    #delete
    def delete(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write('new Nota... forma')

    #modificadores
    def modificadores(self, producto_id):
        producto = Producto.get_by_id(long(producto_id))
        obj = {}
        for modificador in producto.modificadores :
            if modificador.tipo.nombre in obj.keys():
                obj[unicode(modificador.tipo.nombre)].append({
                        'key' : unicode(str(modificador.key())),
                        'nombre': modificador.nombre,
                        'costo': modificador.costo})
            else:
                obj[unicode(modificador.tipo.nombre)] = list([{
                            'key' : unicode(str(modificador.key())),
                            'nombre': modificador.nombre,
                            'costo': modificador.costo}])
        if obj == {}:
            obj = None
        self.render_json(obj)

class ModificadoresProductosHandler(MainHandler):

    def get(self,producto_id):
        producto = Producto.get_by_id(long(producto_id))
        self.respond_to(
            {'json' : (map(lambda m: m.to_dict(include={'modificador': {'tipo':None}}), producto.modificadores))}
            )

    def post(self,producto_id):
        producto = Producto.get_by_id(long(producto_id))
        modificador = Modificador.get_by_id(long(self.request.get('modificador_id')))
        mod_prod = ModificadorProducto()
        mod_prod.producto = producto
        mod_prod.modificador = modificador
        mod_prod.costo = float(self.request.get('costo'))
        mod_prod.put()
        self.respond_to(
            {'json' : mod_prod.to_dict(include={'producto':None})}
            )

    def delete(self, producto_id, modificador_id):
        mod_prod = ModificadorProducto.get_by_id(long(modificador_id))
        mod_prod.delete()
        self.respond_to(
            {'json' : 'ok'}
            )


class ModificadoresHandler(MainHandler):
    # index
    def get(self):
        modificadores = Modificador.all()
        template_values = {
            'modificadores' : modificadores
            }
        self.respond_to(
            {'html' : ('modificadores/index.html',template_values),
             'json' : map(lambda m: m.to_dict(), modificadores)}
            )

    #show
    def show(self,modificador_id):
        modificador = Modificador.get_by_id(long(modificador_id))
        template_values = {
            'modificador' : modificador
            }
        self.render_html('modificadores/edit.html', template_values)
    #new
    def new(self):
        modificador = Modificador()
        tipos_modificador = TipoModificador.all()
        template_values = {
            'modificador' : modificador,
            'tipos_modificador' : tipos_modificador
            }
        self.render_html('modificadores/new.html',template_values)

    #create
    def post(self):
        modificador = Modificador()
        modificador.tipo = TipoModificador.get_by_id(long(self.request.get('tipo_modificador')))
        modificador.nombre = self.request.get('nombre')
        modificador.put()
        self.redirect('/modificadores')

    #edit
    def edit(self, modificador_id):
        modificador = Modificador.get_by_id(long(modificador_id))
        tipos_modificador = TipoModificador.all()
        template_values = {
            'tipos_modificador' : tipos_modificador,
            'modificador' : modificador
            }
        self.render_html('modificadores/edit.html', template_values)

    #update
    def put(self, modificador_id):
        modificador = Modificador.get_by_id(long(modificador_id))
        modificador.nombre = self.request.get('nombre')
        modificador.tipo = TipoModificador.get_by_id(long(self.request.get('tipo_modificador')))
        modificador.put()
        self.redirect('/modificadores')

    #delete
    def delete(self, modificador_id):
        modificador = Modificador.get_by_id(long(modificador_id))
        modificador.delete()
        self.redirect('/modificadores')

class TiposModificadorHandler(MainHandler):
    # index
    def get(self):
        tipos_modificador = TipoModificador.all()
        template_values = {
            'tipos_modificador' : tipos_modificador
            }
        self.respond_to(
            {'html' : ('tipos_modificador/index.html', template_values) },
            {'json' : (map(lambda x: x.to_dict(), tipos_modificador)) }
            )
    #new
    def new(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        tipo_modificador = TipoModificador()
        template_values = {
            'tipo_modificador' : tipo_modificador
            }
        self.render_html('tipos_modificador/new.html',template_values)

    #create
    def post(self):
        tipo_modificador = TipoModificador()
        tipo_modificador.nombre =  self.request.get('nombre')
        tipo_modificador.excluyente = (self.request.get('excluyente') == 'on')
        tipo_modificador.put()
        self.redirect('/tipos_modificador')

    #edit
    def edit(self, tipo_modificador_id):
        tipo_modificador = TipoModificador.get_by_id(int(tipo_modificador_id))
        template_values = {
            'tipo_modificador' : tipo_modificador
            }
        self.render_html('tipos_modificador/edit.html', template_values)

    #update
    def put(self, tipo_modificador_id):
        tipo_modificador = TipoModificador.get_by_id(int(tipo_modificador_id))
        tipo_modificador.nombre =  self.request.get('nombre')
        tipo_modificador.excluyente = (self.request.get('excluyente') == 'on')
        tipo_modificador.put()
        self.redirect('/tipos_modificador')

    #modificadores
    def modificadores(self, tipo_modificador_id):
        tipo_modificador = TipoModificador.get_by_id(long(tipo_modificador_id))
        modificadores = tipo_modificador.modificadores
        template_values = { 'modificadores' : modificadores }
        self.respond_to(
            {'json': (map (lambda modificador: modificador.to_dict(), modificadores )) }
            )



class NotasHandler(MainHandler):
    # index
    def get(self):
        logging.info(datetime.datetime.today())
        delta = datetime.timedelta(hours=-6)
        ahora = datetime.datetime.today() + delta
        if self.request.get('abierta'):
            notas = Nota.gql("WHERE abierta = True")
        elif self.request.get('hora_inicio') and self.request.get('minuto_inicio'):
            hora_inicial = ahora.replace(hour=int(self.request.get('hora_inicio')),minute=int(self.request.get('minuto_inicio')),second=0,microsecond=0)
            nota_gql = Nota.gql("WHERE fecha > :1 AND fecha < :2  ORDER BY fecha", hora_inicial-delta, ahora-delta)
            notas = nota_gql.fetch(limit=50)
        else:
            ahora = ahora.replace(hour=8,minute=0,second=0,microsecond=0)
            notas = Nota.gql("WHERE fecha > :1 AND abierta = False", ahora)
        template_values = {'notas' : notas, 'total_venta' : sum(map(lambda n: n.total, notas)), 'delta_time' : delta }
        self.respond_to(
            {'html': ('notas/index.html', template_values) },
            {'json': (map(lambda nota: nota.to_dict(include={'ordenes': {'producto': None, 'modificadores_producto':
                                                                         {'modificador_producto': {'modificador': None} }}}), notas )) }
            )

    #new
    def new(self):
        nota = Nota()
        nota.put()
        nota.nombre = "Nota_"+str(nota.key().id())
        nota.put()
        self.render_json(nota.to_dict())

    #show
    def show(self, nota_id):
        nota = Nota.get_by_id(long(nota_id))
        template_values = { 'nota' : nota, 'delta' : datetime.timedelta(hours=-6) }
        self.respond_to({'html': ('notas/show.html', template_values) })

    #create
    def post(self):
        nota_json = json.decode(self.request.get('nota'))
        nota = Nota()
        if 'id' in nota_json:
            nota = Nota.get_by_id(long(nota_json['id']))
        nota.total = float(nota_json['total'])
        nota.nombre = nota_json['nombre']
        if 'fecha_impresion' in nota_json:
            nota.fecha_impresion = datetime.datetime.fromtimestamp(float(nota_json['fecha_impresion'])/1000)
        nota.put()
        for orden_json in nota_json['ordenes']:
            orden = Orden()
            if 'id' in orden_json:
                orden = Orden.get_by_id(long(orden_json['id']))
            orden.cantidad = int(orden_json['cantidad'])
            orden.producto = Producto.get_by_id(long(orden_json['producto']['id']))
            orden.nota = nota
            orden.put()
            if 'modificadores_producto' in orden_json:
                for modificador_producto_json in orden_json['modificadores_producto']:
                    if 'id' in modificador_producto_json:
                        orden_modificador_producto = OrdenModificadorProducto.get_by_id(long(modificador_producto_json['id']))
                    else:
                        orden_modificador_producto = OrdenModificadorProducto()
                    orden_modificador_producto.orden = orden
                    orden_modificador_producto.modificador_producto = ModificadorProducto.get_by_id(long(modificador_producto_json['modificador_producto']['id']))
                    orden_modificador_producto.put()

        self.render_json(nota.to_dict())

    #put
    def put(self, nota_id):
        nota =  Nota.get_by_id(long(nota_id))
        if self.request.get('abierta'):
            nota.abierta = self.request.get('abierta') in ("True","true","t")
        if self.request.get('total'):
            nota.total = float(self.request.get('total'))
        nota.put()
        self.render_json(nota.key().id())

    #delete
    def delete(self, nota_id):
        nota = Nota.get_by_id(long(nota_id))
        for orden in nota.ordenes :
            for orden_modificador_producto in orden.modificadores_producto :
                orden_modificador_producto.delete()
            orden.delete()
        nota.delete()
        #TODO Fijar fecha en configuracion... aquí no va.
        delta = datetime.timedelta(hours=-6)
        hoy = datetime.datetime.today().replace(hour=8,minute=0,second=0,microsecond=0)
        notas = Nota.gql("WHERE fecha > :1 AND abierta = False", hoy+delta)
        template_values = {'notas' : notas, 'total_venta' : sum(map(lambda n: n.total, notas)), 'delta_time' : delta }
        self.respond_to(
            {'html': ('notas/index.html', template_values) },
            {'json': (map(lambda nota: nota.to_dict(include={'ordenes': {'producto': None, 'modificadores_producto':
                                                                         {'modificador_producto': {'modificador': None} }}}), notas )) })

    #borrar orden
    def borrar_orden(self, nota_id, orden_id):
        orden = Orden.get_by_id(long(orden_id))
        if orden.modificadores_producto:
            for orden_modificador_producto in orden.modificadores_producto :
                orden_modificador_producto.delete()
        orden.delete()
        self.render_json(orden.key().id())


    def update_orden(self,nota_id, orden_id):
        orden = Orden.get_by_id(long(orden_id))
        orden.cantidad = int(self.request.get('cantidad'))
        orden.put()

    def crea_orden(self,nota_id):
        orden_json = json.decode(self.request.get('orden'))
        logging.info(orden_json)
        #TODO Crear oden en modelo.
        orden = Orden();
        orden.cantidad = orden_json['cantidad']
        orden.llevar = orden_json['llevar']
        orden.producto = Producto.get_by_id(long(orden_json['producto_id']))
        orden.nota = Nota.get_by_id(long(nota_id))
        orden.put()
        if 'modificadores_producto' in orden_json:
            for modificador_producto_json in orden_json['modificadores_producto']:
                orden_modificador_producto = OrdenModificadorProducto()
                orden_modificador_producto.orden = orden
                orden_modificador_producto.modificador_producto = ModificadorProducto.get_by_id(long(modificador_producto_json['id']))
                orden_modificador_producto.put()

        self.render_json(orden.key().id())
