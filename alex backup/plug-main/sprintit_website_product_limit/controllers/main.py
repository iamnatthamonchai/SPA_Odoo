# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.addons.website.models import ir_http

class WebsiteSaleVariantController(WebsiteSaleVariantController):
    
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        res = super(WebsiteSaleVariantController, self).get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        product_obj = request.env['product.template'].browse(product_template_id)
        product_id_obj = request.env['product.product'].browse(product_id)
        website = ir_http.get_request_website()
        product_cart_qty = 0
        if website:
            cart = website.sale_get_order()
            product_cart_qty = sum(cart.order_line.filtered(lambda p: p.product_id.id == product_id_obj.id).mapped('product_uom_qty')) if cart else 0
        res.update({'apply_order_limit': product_obj.apply_order_limit, 'order_limit': product_obj.order_limit, 'display_message' : False, 'product_cart_qty': product_cart_qty}) 
        return res