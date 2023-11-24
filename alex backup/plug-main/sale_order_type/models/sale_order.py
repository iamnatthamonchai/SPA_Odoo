# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.mail import html2plaintext, is_html_empty
import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_order_type(self):
        return self.env['sale.order.type'].search([], limit=1)

    type_id = fields.Many2one(
        comodel_name='sale.order.type', string='Type')

    def _prepare_purchase_order_data(self, company, company_partner):
        res = super(SaleOrder, self)._prepare_purchase_order_data(company,company_partner)
        if self.type_id:
            res['type_id'] = self.type_id.id
        return res

    @api.onchange('type_id')
    def onchange_type_id(self):
        if self.type_id.pricelist_id:
            self.pricelist_id = self.type_id.pricelist_id
        else:
            self.pricelist_id = self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        if 'client_order_ref' in vals:
            for line in result.order_line:
                line.write({'so_reference': vals['client_order_ref']})
        return result

    def write(self,vals):
        res = super().write(vals)
        if 'client_order_ref' in vals:   
            for line in self.order_line:
                if not line.so_reference:
                    line.write({'so_reference': vals['client_order_ref']})
                    client_order_ref = vals['client_order_ref']
                else:
                    client_order_ref = line.so_reference
                moves = self.env['stock.move'].search([('sale_line_id','=',line.id)])
                if moves:
                    for move in moves:
                        picking_description = client_order_ref + ' - '
                        picking_description += line.product_id._get_description(move.picking_type_id)
                        product_description_variants = line._get_sale_order_line_multiline_description_variants()
                        if product_description_variants:
                            picking_description += product_description_variants
                        move.write({'description_picking': picking_description})

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    so_reference = fields.Char(string='SO Reference',copy = False)

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if not line.so_reference:
                line.so_reference = line.order_id.client_order_ref 
        return lines

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        return values


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_order_type(self):
        return self.env['sale.order.type'].search([], limit=1)

    type_id = fields.Many2one(
        comodel_name='sale.order.type', string='Type')

    @api.model
    def create(self, vals):
        result = super(PurchaseOrder, self).create(vals)
        if 'origin' in vals:
            for line in result.order_line:
                line.write({'po_reference': vals['origin']})
        return result

    def write(self,vals):
        res = super().write(vals)
        if 'origin' in vals:   
            for line in self.order_line:
                line.write({'po_reference': vals['origin']})

    def _prepare_sale_order_data(self, name, partner, company, direct_delivery_address):
        res = super(PurchaseOrder, self)._prepare_sale_order_data(name,partner,company,direct_delivery_address)
        if self.type_id:
            res['type_id'] = self.type_id.id
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    po_reference = fields.Char(string='PO Reference',copy = False)

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if not line.po_reference:
                line.po_reference = line.order_id.origin     
        return lines

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        if self.sale_line_id:
            res['sale_line_id'] = self.sale_line_id.id
        return res

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super(StockRule, self)._prepare_purchase_order(company_id, origins, values)
        values = values[0]
        res['type_id'] = values['group_id'].sale_id.type_id.id
        return res

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        if move_values.get('sale_line_id'):
            sale_order_line = self.env['sale.order.line'].browse(move_values.get('sale_line_id'))
            if sale_order_line.so_reference:
                move_values['description_picking'] = sale_order_line.so_reference + " - " + move_values['description_picking']
        return move_values

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    description_invoice = fields.Text('Invoices Description', translate=True)
    description_bill = fields.Text('Bill Description', translate=True)

class Product(models.Model):
    _inherit = "product.product"

    def _get_description(self, picking_type_id):
        """ return product receipt/delivery/picking description depending on
        picking type passed as argument.
        """
        self.ensure_one()
        picking_code = picking_type_id.code
        description = html2plaintext(self.description) if not is_html_empty(self.description) else self.name
        if picking_code == 'incoming':
            return self.description_pickingin or description
        if picking_code == 'outgoing':
            return self.description_pickingout or self.description_sale or self.name
        if picking_code == 'internal':
            return self.description_picking or description