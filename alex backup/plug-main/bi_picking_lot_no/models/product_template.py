# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import Warning


    
class ProductProductInherit(models.Model):
    _inherit = "product.template"

    digits_lot_no = fields.Integer(string='Digits :')
    prefix_lot_no = fields.Char(string="Prefix :")
