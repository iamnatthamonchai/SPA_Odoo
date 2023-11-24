# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLotSize(http.Controller):
#     @http.route('/product_lot_size/product_lot_size', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_lot_size/product_lot_size/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_lot_size.listing', {
#             'root': '/product_lot_size/product_lot_size',
#             'objects': http.request.env['product_lot_size.product_lot_size'].search([]),
#         })

#     @http.route('/product_lot_size/product_lot_size/objects/<model("product_lot_size.product_lot_size"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_lot_size.object', {
#             'object': obj
#         })
