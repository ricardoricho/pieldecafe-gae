import datetime
from google.appengine.ext import db

class MainModel(db.Model):
    def to_dict(self, include=None):
        output = {'id': unicode(self.key().id())}
        for key in self.properties():
            value = getattr(self, key)
            if isinstance(value, MainModel):
                output[key] = unicode(value.key().id())
            elif isinstance(value, datetime.date):
                output[key] = unicode(value)
            elif isinstance(value, db.GeoPt):
                output[key] = {'lat': value.lat, 'lon': value.lon}
            else:
                output[key] = value
        if not include is None :
            for key, prop in include.items() :
                value = getattr(self,key)
                if isinstance(value, MainModel):
                    output[key] = value.to_dict(prop)
                if isinstance(value, db.Query):
                    output[key] = map(lambda x: x.to_dict(prop), value)
        return dict(output)


class Producto(MainModel):
    nombre = db.StringProperty(default='')
    categorias = list(['Bebidas Calientes', 'Bebidas Frias', 'Alimentos'])
    categoria = db.StringProperty(choices=categorias)
    precio = db.FloatProperty(default=0.0)

class TipoModificador(MainModel):
    nombre = db.StringProperty(default='')
    excluyente = db.BooleanProperty()

class Modificador(MainModel):
    nombre = db.StringProperty(default='')
    tipo = db.ReferenceProperty(TipoModificador, collection_name='modificadores')

class ModificadorProducto(MainModel):
    producto = db.ReferenceProperty(Producto, collection_name='modificadores')
    modificador = db.ReferenceProperty(Modificador, collection_name='productos')
    costo = db.FloatProperty(default=0.0)
    default = db.BooleanProperty(default=False)

class Nota(MainModel):
    fecha = db.DateTimeProperty(auto_now_add=True)
    fecha_impresion = db.DateTimeProperty()
    total = db.FloatProperty(default=0.0)
    abierta = db.BooleanProperty(default=True)
    nombre = db.StringProperty(default='')

class Orden(MainModel):
    cantidad = db.IntegerProperty()
    llevar = db.BooleanProperty()
    producto = db.ReferenceProperty(Producto, collection_name='notas')
    nota = db.ReferenceProperty(Nota, collection_name='ordenes')

class OrdenModificadorProducto(MainModel):
    modificador_producto = db.ReferenceProperty(ModificadorProducto, collection_name='ordenes')
    orden = db.ReferenceProperty(Orden, collection_name='modificadores_producto')


