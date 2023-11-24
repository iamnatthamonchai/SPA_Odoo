# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    backend_font_style = fields.Selection([
            ('Odoo', 'Defaults Odoo'),
            ('Bai Jamjuree', 'Bai Jamjuree'),
            ('Chakra Petch', 'Chakra Petch'),
            ('IBM Plex Sans Thai', 'IBM'),
            ('Kanit', 'Kanit'),
            ('Kodchasan', 'Kodchasan'),
            ('Maitree', 'Maitree'),
            ('Mitr', 'Mitr'),
            ('Niramit', 'Niramit'),
            ('Noto Serif Thai', 'Noto'),
            ('Pridi', 'Pridi'),
            ('Prompt', 'Prompt'),
            ('Sarabun', 'Sarabun'),
            ('Taviraj', 'Taviraj'),
            ('Trirong', 'Trirong'),
        ], string='Font Style')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        backend_font_style = ir_config.get_param('backend_font_style', default='Odoo')
        res.update(
            backend_font_style=backend_font_style
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("backend_font_style", self.backend_font_style or "Odoo")
