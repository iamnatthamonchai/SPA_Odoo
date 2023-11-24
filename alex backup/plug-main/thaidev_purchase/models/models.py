# -*- coding: utf-8 -*-

from odoo import models, fields, api
import inflect
from num2words import num2words
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    amount_total_in_words = fields.Char(string="Amount Total in Words", store=True)

    def write(self, values):
        p = inflect.engine()
        if values.get("amount_total"):            
            values["amount_total_in_words"] = p.number_to_words(values["amount_total"])
        else:
            values["amount_total_in_words"] = p.number_to_words(self.amount_total)
        return super(PurchaseOrder, self).write(values)

    def amount_text(self, amount):
        lang = (
            self.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", self.user_id.lang)])
        )
        #langl=self.user_id.lang.iso_code
        try:
            return num2words(amount, to="currency", lang=lang.iso_code)
        except NotImplementedError:
            return num2words(amount, to="currency", lang="en")

# class AccountPayment(models.Model):
#     _inherit = 'account.payment'

#     def  _get_True_floase(self):
#         print("EEEEEEEEEEE")