# -*- coding: utf-8 -*-

from odoo import models


class ThemeElla(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_ella_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
