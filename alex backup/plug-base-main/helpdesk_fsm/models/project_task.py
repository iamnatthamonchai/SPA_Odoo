# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, models, fields


class Task(models.Model):
    _inherit = 'project.task'

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', help='Ticket this task was generated from', readonly=True)

    # Project Sharing fields
    display_helpdesk_ticket_button = fields.Boolean('Display Ticket', compute='_compute_display_helpdesk_ticket_button')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | {'helpdesk_ticket_id', 'display_helpdesk_ticket_button'}

    @api.depends_context('uid')
    @api.depends('helpdesk_ticket_id')
    def _compute_display_helpdesk_ticket_button(self):
        is_portal = self.user_has_groups('base.group_portal')
        if is_portal:
            tickets = self.env['helpdesk.ticket'].search([('id', 'in', self.helpdesk_ticket_id.ids)])
        for task in self:
            task.display_helpdesk_ticket_button = task.helpdesk_ticket_id in tickets if is_portal else bool(task.helpdesk_ticket_id)

    def action_project_sharing_view_ticket(self):
        self.ensure_one()
        if self.env.user.share:
            if not self.display_helpdesk_ticket_button:
                return {}
            return {
                "name": "Portal Ticket",
                "type": "ir.actions.act_url",
                "url": self.helpdesk_ticket_id.get_portal_url(),
            }
        return self.action_view_ticket()

    def write(self, vals):
        previous_states = None
        if 'fsm_done' in vals:
            previous_states = {task: task.fsm_done for task in self}
        res = super().write(vals)
        if 'fsm_done' in vals:
            tracked_tasks = self.filtered(
                lambda t: t.fsm_done and t.helpdesk_ticket_id.use_fsm and previous_states[t] != t.fsm_done)
            subtype = self.env.ref('helpdesk_fsm.mt_ticket_task_done')
            for task in tracked_tasks:
                task.helpdesk_ticket_id.sudo().message_post(
                    subtype_id=subtype.id, body=task._get_html_link())
        return res

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks.filtered('helpdesk_ticket_id'):
            task.message_post_with_view('helpdesk.ticket_creation', values={'self': task, 'ticket': task.helpdesk_ticket_id}, subtype_id=self.env.ref('mail.mt_note').id)
        return tasks
