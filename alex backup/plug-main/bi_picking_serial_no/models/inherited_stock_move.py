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
            digit = result.digits_serial_no
            prefix = result.prefix_serial_no
        else:
            digit = self.product_id.product_tmpl_id.digits_serial_no
            prefix = self.product_id.product_tmpl_id.prefix_serial_no
        serial_no = company.serial_no + 1
        serial_no_digit=len(str(serial_no))

        

        
        diffrence = abs(serial_no_digit - digit)
        if diffrence > 0:
            no = "0"
            for i in range(diffrence-1) :
                no = no + "0"
        else :
            no = ""

        if prefix != False:
            lot_no = prefix+no+str(serial_no)
        else:
            lot_no = str(serial_no)
        company.update({'serial_no' : serial_no})
        lot_name = self.env['stock.production.lot'].search([('name','=',lot_no)])
        if lot_name:
            raise Warning(_('Entered prefix and digit already entered in lot production please entered new data'))
        else:        
            return lot_no    
    
class ProductProductInherit(models.Model):
    _inherit = "product.template"

    digits_serial_no = fields.Integer(string='Digits :')
    prefix_serial_no = fields.Char(string="Prefix :")
