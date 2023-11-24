# -*- coding: utf-8 -*-
from odoo import fields, api, models, _

class res_company(models.Model):
    _inherit ="res.company"

    fax = fields.Char(String='Fax')
    th_name = fields.Char(string="Company Thai Name")
    th_street = fields.Char(string="Company Thai Street", compute=False, inverse=False)
    th_street2 = fields.Char(string="Company Thai Street 2", compute=False, inverse=False)
    th_zip = fields.Char(string="Company Thai Zip", compute=False, inverse=False)
    th_city = fields.Char(string="Company Thai City", compute=False, inverse=False)
    th_state_id = fields.Many2one('res.country.state', string="Company Thai State",compute=False, inverse=False)
    th_country_id = fields.Many2one('res.country', string="Company Thai Country",compute=False, inverse=False)

    def get_company_full_address_text(self):
        address = self.get_company_full_address()
        address_text = ' '.join(address)
        return address_text



    


