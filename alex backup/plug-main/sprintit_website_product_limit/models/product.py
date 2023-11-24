# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import models, fields, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    apply_order_limit = fields.Boolean(string='Apply Order Limit', help="True, If you want to apply product order limit.")
    order_limit = fields.Integer(string='Product Order Limit', default=1, help="Enter number of product which user can order.")