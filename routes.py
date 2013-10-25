import webapp2
from handlers import *


route_list = [
    # Productos
    webapp2.Route(r'/productos', methods=['GET','POST'],
                  handler='handlers.ProductosHandler', name='index-productos'),
    webapp2.Route(r'/productos/new', methods=['GET'],
                  handler='handlers.ProductosHandler:new', name='new-producto'),
    webapp2.Route(r'/productos/<producto_id:\d+>/edit', methods=['GET'],
                  handler='handlers.ProductosHandler:edit', name='edit-producto'),
    webapp2.Route(r'/productos/<producto_id:\d+>', methods=['POST','PUT'],
                  handler='handlers.ProductosHandler:put', name='update-producto'),
    webapp2.Route(r'/productos/<producto_id:\d+>', methods=['GET'],
                  handler='handlers.ProductosHandler:show', name='show-producto'),
    
    # Producto-Modificador
    webapp2.Route(r'/productos/<producto_id:\d+>/modificadores', methods=['GET','POST'],
                  handler='handlers.ModificadoresProductosHandler', name='modificadores-producto'),
    webapp2.Route(r'/productos/<producto_id:\d+>/modificadores/<modificador_id:\d+>', methods=['DELETE','POST'],
                  handler='handlers.ModificadoresProductosHandler:delete', name='delete-modificadores-producto'),
   
    # Tipos de modificador
    webapp2.Route(r'/tipos_modificador', 
                  handler='handlers.TiposModificadorHandler', name='index-tipos_modificador'),
    webapp2.Route(r'/tipos_modificador/new', 
                  handler='handlers.TiposModificadorHandler:new', name='new-tipos_modificador'),
    webapp2.Route(r'/tipos_modificador/<tipo_modificador_id:\d+>', methods=['POST','PUT'],
                  handler='handlers.TiposModificadorHandler:put', name='update-tipos_modificador'),
    webapp2.Route(r'/tipos_modificador/<tipo_modificador_id:\d+>', 
                  handler='handlers.TiposModificadorHandler:show', name='show-tipos_modificador'),
    webapp2.Route(r'/tipos_modificador/<tipo_modificador_id:\d+>/edit', 
                  handler='handlers.TiposModificadorHandler:edit', name='edit-tipos_modificador'),
    
    # TipoModificdor - Modificador
    webapp2.Route(r'/tipos_modificador/<tipo_modificador_id:\d+>/modificadores', methods=['GET','POST'],
                  handler='handlers.TiposModificadorHandler:modificadores', 
                  name='modificadores-tipos_modificador'),
   
    # Modificadores
    webapp2.Route(r'/modificadores', 
                  handler='handlers.ModificadoresHandler', name='index-modificadores'),
    webapp2.Route(r'/modificadores/new', 
                  handler='handlers.ModificadoresHandler:new', name='new-modificadores'),
    webapp2.Route(r'/modificadores/<modificador_id:\d+>/edit', 
                  handler='handlers.ModificadoresHandler:edit', name='edit-modificadores'),
    webapp2.Route(r'/modificadores/<modificador_id:\d+>', methods = ['POST','PUT'],
                  handler='handlers.ModificadoresHandler:put', name='update-modificadores'),
    webapp2.Route(r'/modificadores/<modificador_id:\d+>', methods = ['POST','DELETE'],
                  handler='handlers.ModificadoresHandler:delete', name='delete-modificadores'),
    webapp2.Route(r'/modificadores/<modificador_id:\d+>', 
                  handler='handlers.ModificadoresHandler:show', name='show-modificadores'),
  
    # Notas
    webapp2.Route(r'/notas', 
                  handler='handlers.NotasHandler', name='index-nota'),
    webapp2.Route(r'/notas/new', 
                  handler='handlers.NotasHandler:new', name='new-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>/ordenes/<orden_id:\d+>', methods=['DELETE'], 
                  handler='handlers.NotasHandler:borrar_orden', name='borrar_orden-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>/ordenes/', methods=['POST'], 
                  handler='handlers.NotasHandler:crea_orden', name='borrar_orden-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>/ordenes/<orden_id:\d+>', methods=['PUT'], 
                  handler='handlers.NotasHandler:update_orden', name='modifica_orden-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>', methods=['PUT','POST'],
                  handler='handlers.NotasHandler:put', name='update-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>', methods=['DELETE','POST'],
                  handler='handlers.NotasHandler:delete', name='delete-nota'),
    webapp2.Route(r'/notas/<nota_id:\d+>', 
                  handler='handlers.NotasHandler:show', name='show-nota'),
    
    
    # Root
    (r'/', MainHandler)
    ]
