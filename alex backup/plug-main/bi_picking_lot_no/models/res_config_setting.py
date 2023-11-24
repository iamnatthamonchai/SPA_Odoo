# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Company(models.Model):
	_inherit = 'res.company'


	lot_no = fields.Integer(default = 0)
	digits_lot_no = fields.Integer(string='Digits :')
	prefix_lot_no = fields.Char(string="Prefix :")


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	apply_method = fields.Selection([("global","Global"),("product_wise",'Product wise')],'Lot Number Apply Method',default="global")
	digits_lot_no = fields.Integer(string='Digits :',related="company_id.digits_lot_no",readonly=False)
	prefix_lot_no = fields.Char(string="Prefix :",related="company_id.prefix_lot_no",readonly=False)


	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(apply_method = self.env['ir.config_parameter'].sudo().get_param('bi_picking_lot_no.apply_method'))
		return res


	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('bi_picking_lot_no.apply_method', self.apply_method)



