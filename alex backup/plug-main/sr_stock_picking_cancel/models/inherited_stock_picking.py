# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def picking_cancel(self):
        for move in self.move_ids_without_package:
            move_line = []
            if move.product_id.type == "product":
                if move.picking_id.picking_type_id.code == "outgoing":
                    for line in move.move_line_ids:
                        if move.product_id.tracking == "none":
                            quant = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", line.product_id.id),
                                    ("location_id", "=", line.location_id.id),
                                    ("package_id", "=", line.package_id.id),
                                    ("lot_id", "=", line.lot_id.id),
                                ],
                                limit=1,
                            )
                            lot_id = line.lot_id
                            in_date = None
                            quant.with_context(
                                {"move_line_id": line}
                            )._update_available_quantity(
                                line.product_id,
                                line.location_id,
                                line.qty_done,
                                line.lot_id,
                                line.package_id,
                                line.owner_id,
                                in_date,
                            )
                        else:
                            quant = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", line.product_id.id),
                                    ("location_id", "=", line.location_id.id),
                                    ("package_id", "=", line.package_id.id),
                                    ("lot_id", "=", line.lot_id.id),
                                ],
                                limit=1,
                            )
                            in_date = None
                            quant.with_context(
                                {"move_line_id": line}
                            )._update_available_quantity(
                                line.product_id,
                                line.location_id,
                                line.qty_done,
                                line.lot_id,
                                line.package_id,
                                line.owner_id,
                                in_date,
                            )
                if move.picking_id.picking_type_id.code == "incoming":
                    if move.product_id.tracking == "none":
                        quant = self.env["stock.quant"].search(
                            [
                                ("product_id", "=", move.product_id.id),
                                ("location_id", "=", move.location_dest_id.id),
                            ],
                            limit=1,
                        )
                        quant._update_available_quantity(
                            move.product_id, move.location_dest_id, -move.quantity_done
                        )
                    else:
                        for line in move.move_line_ids:
                            quant = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", move.product_id.id),
                                    ("location_id", "=", move.location_dest_id.id),
                                    ("lot_id", "=", line.lot_id.id),
                                ],
                                limit=1,
                            )
                            lot_id = line.lot_id
                        quant._update_available_quantity(
                            move.product_id,
                            move.location_dest_id,
                            -move.quantity_done,
                            line.lot_id,
                        )

                if move.picking_id.picking_type_id.code == "internal":
                    in_date = fields.Datetime.now()
                    for move_line in move.move_line_ids.filtered(
                        lambda x: x.product_id == move.product_id
                    ):

                        if move_line.product_id.tracking == "none":

                            Quant = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", move_line.product_id.id),
                                    ("location_id", "=", move_line.location_id.id),
                                    ("package_id", "=", move_line.package_id.id),
                                ],
                                limit=1,
                            )

                            Quant._update_available_quantity(
                                move_line.product_id,
                                move_line.location_id,
                                move_line.qty_done,
                                lot_id=False,
                                package_id=move_line.package_id,
                                owner_id=move_line.owner_id,
                                in_date=in_date,
                            )

                            Quant_ = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", move_line.product_id.id),
                                    ("location_id", "=", move_line.location_dest_id.id),
                                    ("package_id", "=", move_line.result_package_id.id),
                                ],
                                limit=1,
                            )

                            Quant_._update_available_quantity(
                                move_line.product_id,
                                move_line.location_dest_id,
                                -move_line.qty_done,
                                lot_id=False,
                                package_id=move_line.result_package_id,
                                owner_id=move_line.owner_id,
                                in_date=in_date,
                            )
                        else:
                            Quant = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", move_line.product_id.id),
                                    ("location_id", "=", move_line.location_id.id),
                                    ("package_id", "=", move_line.package_id.id),
                                ],
                                limit=1,
                            )
                            Quant._update_available_quantity(
                                move_line.product_id,
                                move_line.location_id,
                                -move_line.qty_done,
                                lot_id=move_line.lot_id,
                                package_id=move_line.package_id,
                                owner_id=move_line.owner_id,
                                in_date=in_date,
                            )

                            Quant_ = self.env["stock.quant"].search(
                                [
                                    ("product_id", "=", move_line.product_id.id),
                                    ("location_id", "=", move_line.location_dest_id.id),
                                    ("package_id", "=", move_line.result_package_id.id),
                                ],
                                limit=1,
                            )
                            Quant_._update_available_quantity(
                                move_line.product_id,
                                move_line.location_dest_id,
                                move_line.qty_done,
                                lot_id=move_line.lot_id,
                                package_id=move_line.result_package_id,
                                owner_id=move_line.owner_id,
                                in_date=in_date,
                            )
            valuation_id = self.env["stock.valuation.layer"].search(
                [("stock_move_id", "=", move.id)], limit=1
            )
            is_cancel = move.sudo()._action_cancel()
            if is_cancel:
                valuation_id.write(
                    {
                        "quantity": 0.0,
                        "unit_cost": 0.0,
                        "value": 0.0,
                        "remaining_qty": 0.0,
                    }
                )
                valuation_id.account_move_id.button_cancel()
        self.write({"state": "cancel"})
        return


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_cancel(self):
        print("__action_cancel__ self._context : ", self._context)
        if self._context.get("update_stock", False):
            moves_to_cancel = self.filtered(lambda m: m.state != "cancel")
            # self cannot contain moves that are either cancelled or done, therefore we can safely
            # unlink all associated move_line_ids
            moves_to_cancel.with_context(stock_cancel=True)._do_unreserve()

            for move in moves_to_cancel:
                siblings_states = (
                    move.move_dest_ids.mapped("move_orig_ids") - move
                ).mapped("state")
                if move.propagate_cancel:
                    # only cancel the next move if all my siblings are also cancelled
                    if all(state == "cancel" for state in siblings_states):
                        move.move_dest_ids.filtered(
                            lambda m: m.state != "done"
                        )._action_cancel()
                else:
                    if all(state in ("done", "cancel") for state in siblings_states):
                        move.move_dest_ids.write({"procure_method": "make_to_stock"})
                        move.move_dest_ids.write({"move_orig_ids": [(3, move.id, 0)]})
            self.write(
                {
                    "state": "cancel",
                    "move_orig_ids": [(5, 0, 0)],
                    "procure_method": "make_to_stock",
                }
            )
            return True
        else:
            return super(StockMove, self)._action_cancel()

    def _do_unreserve(self):
        # print ('_do_unreserve___ self._context : ', self._context)
        moves_to_unreserve = self.env["stock.move"]
        if self._context.get("update_stock"):
            for move in self:
                moves_to_unreserve |= move
            # print ('___ moves_to_unreserve : ', moves_to_unreserve)
            print(
                "___ moves_to_unreserve.with_context(prefetch_fields=True,update_stock=True).mapped(move_line_ids) : ",
                moves_to_unreserve.with_context(
                    prefetch_fields=True, update_stock=True
                ).mapped("move_line_ids"),
            )
            moves_to_unreserve.with_context(
                prefetch_fields=True, update_stock=True
            ).mapped("move_line_ids").unlink()
            return True
        else:
            return super(StockMove, self)._do_unreserve()


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        pass

    def unlink(self):
        print("unlink___ self._context : ", self._context)
        if self._context.get("update_stock"):

            for ml in self:
                if ml.product_id.type == "product":
                    try:
                        self.env["stock.quant"].with_context(
                            update_stock=True
                        )._update_reserved_quantity(
                            ml.product_id,
                            ml.location_id,
                            -ml.product_qty,
                            lot_id=ml.lot_id,
                            package_id=ml.package_id,
                            owner_id=ml.owner_id,
                            strict=True,
                        )
                    except UserError:
                        if ml.lot_id:
                            self.env["stock.quant"]._update_reserved_quantity(
                                ml.product_id,
                                ml.location_id,
                                -ml.product_qty,
                                lot_id=False,
                                package_id=ml.package_id,
                                owner_id=ml.owner_id,
                                strict=True,
                            )
                        else:
                            raise

            moves = self.mapped("move_id")
            if moves:
                moves._recompute_state()
            return models.Model.unlink(self)
        else:
            return super(StockMoveLine, self).unlink()


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _unlink_zero_quants(self):
        """_update_available_quantity may leave quants with no
        quantity and no reserved_quantity. It used to directly unlink
        these zero quants but this proved to hurt the performance as
        this method is often called in batch and each unlink invalidate
        the cache. We defer the calls to unlink in this method.
        """
        precision_digits = max(
            6, self.sudo().env.ref("product.decimal_product_uom").digits * 2
        )
        # Use a select instead of ORM search for UoM robustness.
        query = """SELECT id FROM stock_quant WHERE (round(quantity::numeric, %s) = 0 OR quantity IS NULL) AND round(reserved_quantity::numeric, %s) = 0;"""
        params = (precision_digits, precision_digits)
        self.env.cr.execute(query, params)
        quant_ids = self.env["stock.quant"].browse(
            [quant["id"] for quant in self.env.cr.dictfetchall()]
        )

        quant_obj = self.env["stock.quant"]

        for quant_id in quant_ids:
            if not quant_id.package_id:
                quant_obj += quant_id
        quant_obj.sudo().unlink()

    @api.model
    def _update_available_quantity(
        self,
        product_id,
        location_id,
        quantity,
        lot_id=None,
        package_id=None,
        owner_id=None,
        in_date=None,
    ):
        move_line = self._context.get("move_line_id")
        if move_line:
            product_id = move_line.product_id
            location_id = move_line.location_id
            quantity = move_line.qty_done
            lot_id = move_line.lot_id
            package_id = move_line.package_id
            owner_id = move_line.owner_id
            in_date = None
        return super(StockQuant, self)._update_available_quantity(
            product_id, location_id, quantity, lot_id, package_id, owner_id, in_date
        )
