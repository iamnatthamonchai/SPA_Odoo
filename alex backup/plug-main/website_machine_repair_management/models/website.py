# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    def get_product_list(self):
        product_ids = self.env['product.product'].search(
            [('sale_ok', '=', 'True'), ("website_published", "=", True), ('machine', '=', 'True')])
        return product_ids

    def get_customer_list(self):
        partners_ids = self.env['res.partner'].search([('customer', '=', 'True')])
        return partners_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
