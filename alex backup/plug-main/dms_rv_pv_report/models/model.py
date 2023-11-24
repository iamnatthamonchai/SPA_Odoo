# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from bahttext import bahttext


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def return_bahttext(self , amount):
        #bahttext_text = bahttext(amount)
        #return bahttext_text
        return amount
