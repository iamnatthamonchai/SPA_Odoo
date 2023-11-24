# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import models, _
        
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        try:
            if add_qty:
                add_qty = int(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = int(set_qty)
        except ValueError:
            set_qty = 0
        product = self.env['product.product'].browse(product_id)
        order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1]
        warning = ''
        if set_qty and set_qty > 0 and product.order_limit:
            if set_qty >= product.order_limit:
                warning = _('You ask for %s products but only %s is Purchasable.') % (set_qty, product.order_limit)
                set_qty = product.order_limit
                order_line.write({'product_uom_qty': product.order_limit})

        res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        res['warning'] = warning
        return res
        