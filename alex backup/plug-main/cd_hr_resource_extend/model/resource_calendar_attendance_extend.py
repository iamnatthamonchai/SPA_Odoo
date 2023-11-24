from odoo import models, fields, api, _


class ResourceCalendarAttendance(models.Model):
    _inherit = "resource.calendar.attendance"


    day_period = fields.Selection(selection_add=[('night', 'Night')],ondelete={'night': 'cascade'})
