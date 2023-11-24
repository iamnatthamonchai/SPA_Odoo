# -*- coding: utf-8 -*-

from odoo import models, fields, api
import inflect

import logging
_logger = logging.getLogger(__name__)

"""
pip3 install importlib-metadata
pip3 install zipp
pip3 install inflect

Then in your Python session

import inflect
p = inflect.engine()
p.number_to_words(1234567)
        'one million, two hundred and thirty-four thousand, five hundred and sixty-seven'

p.number_to_words(22)
        'twenty-two' 
"""

class AccountMove(models.Model):
    _inherit = "account.move"
    
    amount_total_in_words = fields.Char(string="Amount Total in Words", store=True)
    internat_note = fields.Char(string="Internal Note", store=True)
    
    def write(self, values):
        p = inflect.engine()
        if values.get("amount_total"):            
            values["amount_total_in_words"] = p.number_to_words(values["amount_total"])
        else:
            values["amount_total_in_words"] = p.number_to_words(self.amount_total)
        return super(AccountMove, self).write(values)



class Company(models.Model):
    _inherit = "res.company"

    invoice_company_colour = fields.Char(string="Invoice Company Colour")
    invoice_customer_colour = fields.Char(string="Invoice Customer Colour")
    invoice_accounts_colour = fields.Char(string="Invoice Accounts Colour")
    

