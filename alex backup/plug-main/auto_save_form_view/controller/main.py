
from odoo import http, _
from odoo.http import request


class AutoSaveFormView(http.Controller):
    @http.route('/auto_save/data', type='json', auth='user')
    def base_setup_data(self, **kwargs):
        res = {}

        save_timer = request.env['ir.config_parameter'].sudo().get_param('auto_save_timer_key')
        auto_save_new_form = request.env['ir.config_parameter'].sudo().get_param('auto_save_new_form')
        auto_save_any_state = request.env['ir.config_parameter'].sudo().get_param('auto_save_any_state')

        res.update({
            'save_timer': save_timer if save_timer else 30,
            'auto_save_new_form': auto_save_new_form,
            'auto_save_any_state': auto_save_any_state,
        })

        return res
