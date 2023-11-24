# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import clean_context, OrderedSet


class StockMove(models.Model):
	_inherit = "stock.move"


	def _action_done(self, cancel_backorder=False):
		moves_todo = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
		if moves_todo:
			picking_id = self.picking_id
			if picking_id:
				moves_todo.write({'state': 'done', 'date': fields.Datetime.now()})
			else:
				moves_todo.write({'state': 'done', 'date': fields.Datetime.now()})
		return moves_todo