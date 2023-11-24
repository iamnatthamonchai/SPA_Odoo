from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit')], 'Bundle Type',
        default='kit', required=True)

    bundle_pack = fields.Boolean(string='Is Bundle', default=False, copy=False)

    @api.onchange('bundle_pack')
    def onchange_bundle_pack(self):
        for rec in self:
            if rec.bundle_pack == True:
                rec.type = 'phantom'
            else:
                rec.type = False

    @api.onchange('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'normal':
                raise UserError(_('Sorry You are not allow set to Manufacture This Product'))
