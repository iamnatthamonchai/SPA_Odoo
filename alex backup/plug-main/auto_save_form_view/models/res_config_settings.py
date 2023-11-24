from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_save_new_form = fields.Boolean("Auto Save New Form.",
                config_parameter='auto_save_new_form',
                help="""Auto save the new form, if this option is selected.""")

    auto_save_any_state = fields.Boolean("Auto Save With Any State.",
                                        config_parameter='auto_save_any_state',
                                        help="""The form will be saved automatically, if the form has any state.
                                        Otherwise, only draft state will be saved.""")
