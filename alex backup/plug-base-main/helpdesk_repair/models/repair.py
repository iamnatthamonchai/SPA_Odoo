# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Repair(models.Model):
    _inherit = 'repair.order'

    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket", help="Related Helpdesk Ticket")

    def write(self, vals):
        previous_states = None
        if 'state' in vals:
            previous_states = {repair: repair.state for repair in self}
        res = super().write(vals)
        if 'state' in vals:
            tracked_repairs = self.filtered(
                lambda r: r.ticket_id.use_product_repairs and r.state in ('done', 'cancel') and previous_states[r] != r.state)
            for repair in tracked_repairs:
                subtype = self.env.ref('helpdesk.mt_ticket_repair_' + repair.state, raise_if_not_found=False)
                if not subtype:
                    continue
                body = f"{repair._get_html_link()} {subtype.name}"
                repair.ticket_id.sudo().message_post(subtype_id=subtype.id, body=body)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders.filtered('ticket_id'):
            order.message_post_with_view('helpdesk.ticket_creation', values={'self': order, 'ticket': order.ticket_id}, subtype_id=self.env.ref('mail.mt_note').id)
        return orders

    def action_repair_done(self):
        """repair.action_repair_done() calls stock_move.create() which,
        if default_lot_id is still in the context, will give all stock_move_lines.lot_id this value.
        We want to avoid that, as the components of the repair do not have the same lot_id, if any,
        so it leads to an exception.
        """
        context = dict(self.env.context)
        context.pop('default_lot_id', None)
        return super(Repair, self.with_context(context)).action_repair_done()
