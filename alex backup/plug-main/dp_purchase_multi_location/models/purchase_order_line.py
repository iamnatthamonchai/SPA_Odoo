# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    location_dest_id = fields.Many2one('stock.location', string="Destination Location", domain=[("usage", "in", ["internal", "transit"])])

    def _create_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._create_stock_moves(picking)
        for line in self:
            location = line.order_id._get_destination_location()
            if line.location_dest_id:
                location = line.location_dest_id.id
            if location:
                line.move_ids.filtered(lambda m: m.state != "done").write({'location_dest_id': location})
        return res
