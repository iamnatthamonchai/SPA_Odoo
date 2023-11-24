from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    wt_tax_amount = fields.Float(
        string="WHT Amount",
    )

    @api.onchange("invoice_line_ids")
    def compute_wt_tax(self):
        _logger.info("Amount total")
        for rec in self:
            amount_wt_tax = 0
            for invoice_line in rec.invoice_line_ids:
                _logger.info(invoice_line)
                if invoice_line.wt_tax_id:
                    _logger.info(invoice_line.wt_tax_id)
                    wt_tax_id = self.env["account.withholding.tax"].search([('id','=',invoice_line.wt_tax_id.id)])
                    _logger.info(wt_tax_id)
                    amount_line_wt_tax = (invoice_line.price_subtotal * wt_tax_id.amount)/100
                    amount_wt_tax += amount_line_wt_tax
            self.wt_tax_amount = amount_wt_tax

