# -*- coding: utf-8 -*-
import logging
from odoo import http, SUPERUSER_ID
from odoo.http import request, JsonRequest, Response
from odoo.tools import date_utils
import json

_logger = logging.getLogger(__name__)

class bfsConfig(http.Controller):
    @http.route('/bfs_config', type="json", auth='public', csrf=False)
    def bfs_config(self):
        backend_font_style = request.env['ir.config_parameter'].sudo().get_param('backend_font_style', default='Odoo')
        response = {
            "backend_font_style": backend_font_style
        }
        return response