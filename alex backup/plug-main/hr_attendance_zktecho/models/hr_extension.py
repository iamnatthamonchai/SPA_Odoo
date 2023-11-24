# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,UserError
#import datetime
#from pytz import timezone, UTC

class HrAttendance(models.Model):
    
    _name = 'hr.attendance'
    _inherit = ['hr.attendance','mail.thread']
    
    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    
    name = fields.Datetime('Datetime')
    day = fields.Date("Day")
    is_missing = fields.Boolean('Missing', default=False)
    employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True, ondelete='cascade', index=True, track_visibility='onchange')
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True, track_visibility='onchange')
    check_out = fields.Datetime(string="Check Out", track_visibility='onchange')


class hrDraftAttendance(models.Model):

    _name = 'hr.draft.attendance'
    _inherit = ['mail.thread']
    _order = 'name desc'
    

    name = fields.Datetime('Datetime', required=False,track_visibility='onchange')
    date = fields.Date('Date', required=False,track_visibility='onchange')
    day_name = fields.Char('Day',track_visibility='onchange')
    attendance_status = fields.Selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('sign_none', 'None')], 'Attendance State', required=True,track_visibility='onchange')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee',track_visibility='onchange')
    lock_attendance = fields.Boolean('Lock Attendance',track_visibility='onchange')
    biometric_attendance_id = fields.Integer(string='Biometric Attendance ID',track_visibility='onchange')
    is_missing = fields.Boolean('Missing', default=False,track_visibility='onchange')
    moved = fields.Boolean(default=False)
    moved_to = fields.Many2one(comodel_name='hr.attendance', string='Moved to HR Attendance')
    
    def unlink(self):
        for rec in self:
            if rec.moved == True:
                raise UserError(_("You can`t delete Moved Attendance"))
        return super(hrDraftAttendance, self).unlink()
    
    #time = fields.Float('Time', compute='_compute_time', store=True)
    #
    #@api.depends('name')
    #def _compute_time(self):
    #    for rec in self:
    #        if rec.name:
    #            user = self.env['res.users'].search([('active','=',True)], limit=1, order='id asc')
    #            tz = user.tz if user.tz else 'UTC'
    #            local_tz = timezone(tz)
    #            dt = rec.name.replace(tzinfo=UTC)
    #            dt = dt.astimezone(timezone(tz))
    #            time = dt.hour+dt.minute/60.0
    #            rec.time = time


class Employee(models.Model):
    
    _inherit = 'hr.employee'
    
    is_shift = fields.Boolean("Shifted Employee")
    attendance_devices = fields.One2many(comodel_name='employee.attendance.devices', inverse_name='name', string='Attendance Devices')
    draft_attendances = fields.One2many(comodel_name='hr.draft.attendance', inverse_name='employee_id', string='Draft Attendances')
    draft_attendances_not_moved = fields.One2many(comodel_name='hr.draft.attendance', compute='_get_draft_attendance', string='Draft Attendances', store=False)
    last_draft_attendance_id = fields.Many2one('hr.draft.attendance', compute='_compute_last_draft_attendance_id')

    @api.depends('draft_attendances')
    def _compute_last_draft_attendance_id(self):
        for employee in self:
            employee.last_draft_attendance_id = employee.draft_attendances and employee.draft_attendances[0] or False

    @api.depends('last_draft_attendance_id.attendance_status', 'last_draft_attendance_id', 'last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_state(self):
        for employee in self:
            if employee.last_attendance_id and not employee.last_attendance_id.zkteco_device_attendance:
                employee.attendance_state = employee.last_attendance_id and not employee.last_attendance_id.check_out and 'checked_in' or 'checked_out'
            else:
                _logger.info('Computing attendance state for employee ' + str(employee))
                attendance_state = 'checked_out'
                if employee.last_draft_attendance_id and employee.last_draft_attendance_id.attendance_status == 'sign_in':
                    _logger.info('    check in found for employee ' + str(employee) + ' -- ' + str(employee.last_draft_attendance_id))
                    attendance_state = 'checked_in'
                employee.attendance_state = attendance_state
            
    def _get_draft_attendance(self):
        #_logger.info(self._context)
        draft_start_date = self._context.get('draft_start_date', False)
        draft_end_date = self._context.get('draft_end_date', False)
        search_domain = [('employee_id', '=', self.id), ('moved', '=', False)]
        if draft_start_date:
            search_domain.append(('name', '>=', draft_start_date))
        if draft_end_date:
            search_domain.append(('name', '<=', draft_end_date))
        #_logger.info(search_domain)
        self.draft_attendances_not_moved = self.env['hr.draft.attendance'].search(search_domain)
    

class EmployeeAttendanceDevices(models.Model):
    
    _name = 'employee.attendance.devices'
    _description = 'Employee Attendance Devices'
    
    name = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    attendance_id = fields.Char("Attendance ID", required=True)
    device_id = fields.Many2one(comodel_name='biomteric.device.info', string='Biometric Device', required=True, ondelete='restrict')
    
    @api.constrains('attendance_id', 'device_id', 'name')
    def _check_unique_constraint(self):
        self.ensure_one()
        record = self.search([('attendance_id', '=', self.attendance_id), ('device_id', '=', self.device_id.id)])
        if len(record) > 1:
            raise ValidationError('Employee with Id ('+ str(self.attendance_id)+') exists on Device ('+ str(self.device_id.name)+') !')
        record = self.search([('name', '=', self.name.id), ('device_id', '=', self.device_id.id)])
        if len(record) > 1:
            raise ValidationError('Configuration for Device ('+ str(self.device_id.name)+') of Employee  ('+ str(self.name.name)+') already exists!')
