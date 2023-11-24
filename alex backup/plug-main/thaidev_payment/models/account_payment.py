# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import _, fields, models, api
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    invoice_detail = fields.Char("Detail from invoice",compute='_get_account_detail',default=' ')

    @api.model
    def _get_account_detail(self):
        self.invoice_detail = ' '
        account_move_line = self.env["account.move.line"].search([('move_name','=',self.communication),('price_total','>',0)],limit=5,order='id asc')
        if account_move_line :
            for move_line in account_move_line:
                if move_line.name:
                    self.invoice_detail = str(move_line.name) +' '+ str(self.invoice_detail)+ '</p>'                    
                elif move_line.name == False :
                    move_line_empty = ' '  
                    self.invoice_detail = move_line_empty + ' '+ str(self.invoice_detail)+ '</p>'
                else:
                    move_line_empty = ' '  
                    self.invoice_detail = move_line_empty + ' '+ str(self.invoice_detail)+ '</p>'
        else :
            self.invoice_detail = self.communication

        


