# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import Warning


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity , reserved_quant)
        if self.picking_id.picking_type_code == "incoming":
            if self.product_id.tracking == "serial":
                lot_serial_no_id = self.create_serial_no_stock()
                vals.update({
                    'lot_name' : lot_serial_no_id,
                    'product_uom_qty' : 0.0,
                    'qty_done' : 1
                    })   
            elif self.product_id.tracking == "lot":
                lot_serial_no_id = self.create_serial_no_stock()
                vals.update({
                    'lot_name' : lot_serial_no_id,
                    'product_uom_qty' : 0.0,
                    'qty_done' : self.product_uom_qty
                    })
        return vals


    def create_serial_no_stock(self):
        company = self.env.user.company_id
        result = self.env['res.config.settings'].sudo().search([],order="id desc", limit=1)
        if result.apply_method == "global":
            digit = result.digits_lot_no
            prefix = result.prefix_lot_no
        else:
            digit = self.product_id.product_tmpl_id.digits_lot_no
            prefix = self.product_id.product_tmpl_id.prefix_lot_no
        lot_no = company.lot_no + 1
        lot_no_digit=len(str(lot_no))

        diffrence = abs(lot_no_digit - digit)
        if diffrence > 0:
            no = "0"
            for i in range(diffrence-1) :
                no = no + "0"
        else :
            no = ""

        if prefix != False:
            serial_no = prefix+no+str(lot_no)
        else:
            serial_no = str(lot_no)
        company.update({'lot_no' : lot_no})
        lot_name = self.env['stock.production.lot'].search([('name','=',serial_no)])
        if lot_name:
            raise Warning(_('Entered prefix and digit already entered in lot production please entered new data'))
        else:        
            return serial_no    
    
