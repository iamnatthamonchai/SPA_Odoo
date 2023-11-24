# -*- coding: utf-8 -*-

import datetime
from pytz import timezone, all_timezones
import logging
_logger = logging.getLogger('biometric_device')
from .zk import ZK
from .zk.exception import ZKErrorResponse, ZKNetworkError


#try:
#    from zk3 import ZK
#except ImportError:
#    raise ImportError('This module needs pyzk3 to fetch attendance from zk devices in Odoo.')


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning
from socket import timeout

class BiomtericDeviceInfo(models.Model):

    _name = 'biomteric.device.info'
    _inherit = ['mail.thread']

    @api.model
    def fetch_attendance(self):
        machines = self.search([])
        for machine in machines:
            #if machine.apiversion == 'ZKLib':
            try:
                machine.download_attendance_oldapi()
                self._cr.commit()
            except:
                _logger.warning("can't reach device '%s'" % machine.name)
            
    def test_connection_device(self):
        #zk = ZK(self.ipaddress, int(self.portnumber), timeout=90)
        force_udp = False
        if self.protocol == 'udp':
            force_udp = True
        password = self.password or 0
        ommit_ping = self.ommit_ping
        zk = ZK(self.ipaddress, port=int(self.portnumber), timeout=60, password=password, force_udp=force_udp, ommit_ping=ommit_ping)
        res = None
        try:
            res = zk.connect()
            if not res:
                raise Warning('Connection Failed to Device '+str(self.name))
            else:
                raise Warning('Connection Successful '+str(self.name))
        except ZKNetworkError as e:
            if e.args[0] == "can't reach device (ping %s)" % self.ipaddress:
                raise Warning("can't reach device (ping %s), make sure the device is powered on and connected to the network" % self.ipaddress)
            else:
                raise Warning(e)
        except ZKErrorResponse as e:
            if e.args[0] == 'Unauthenticated':
                raise Warning("Unable to connect (Authentication Failure), Kindly supply correct password for the device.")
            else:
                raise Warning(e)
        except timeout:
            raise Warning("Connection timed out, make sure the device is turned on and not blocked by the Firewall")
        except Exception as e:
            raise Warning(e)
        finally:
            if res:
                res.disconnect()

    def get_local_utc(self, offset):
   
        hours = offset[1:3]
        minutes = offset[3:5]
        return [int(hours),int(minutes)]

    def download_attendance_oldapi(self):
        _logger.info('Fetching attendance')
        if self.fetch_days >= 0:
            now_datetime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            prev_datetime = now_datetime - datetime.timedelta(days=self.fetch_days)
            curr_date = prev_datetime.date() 
        else:
            curr_date = datetime.datetime.strptime('1950-01-01','%Y-%m-%d')
        
        conn = None
        password = self.password or 0
        force_udp = False
        if self.protocol == 'udp':
            force_udp = True
        ommit_ping = self.ommit_ping
        zk = ZK(self.ipaddress, port=int(self.portnumber), timeout=60, password=password, force_udp=force_udp, ommit_ping=ommit_ping)
        
        #zk = ZK(self.ipaddress, int(self.portnumber), timeout=90)
        try:
            conn = zk.connect()
            conn.disable_device()
            attendance = conn.get_attendance()
            conn.enable_device()
            if (attendance):
                if self.fetch_days > 0:
                    now_datetime = conn.get_time()
                    prev_datetime = now_datetime - datetime.timedelta(days=self.fetch_days)
                    curr_date = prev_datetime.date()
                hr_attendance =  self.env['hr.draft.attendance']
                for lattendance in attendance:

                    _logger.info('Status: ' + str(lattendance.status) + ', Punch: ' + str(lattendance.punch))
                    #_logger.info(str(lattendance.puch))
                    _logger.info(lattendance)
                    
                    #curr_date = '2017-10-31'
                    if str(curr_date) <= str(lattendance.timestamp.date()):
                        my_local_timezone = timezone(self.time_zone)
                        local_date = my_local_timezone.localize(lattendance.timestamp)
                        utcOffset = local_date.strftime('%z')
                        hours , minutes = self.get_local_utc(utcOffset)
                        time_att = str(lattendance.timestamp.date()) + ' ' +str(lattendance.timestamp.time())
                        atten_time1 = datetime.datetime.strptime(str(time_att), '%Y-%m-%d %H:%M:%S')
                        if utcOffset[0] == '+':
                            atten_time = atten_time1 - datetime.timedelta(hours=hours,minutes=minutes)
                        elif utcOffset[0] == '-':
                            atten_time = atten_time1 + datetime.timedelta(hours=hours,minutes=minutes)
                        else:
                            atten_time = atten_time1
                        atten_time = datetime.datetime.strftime(atten_time, '%Y-%m-%d %H:%M:%S')
                        att_id = lattendance.user_id
                        if att_id:
                            att_id = str(att_id)
                        else:
                            att_id = ''
                        employees = self.env['employee.attendance.devices'].search([('attendance_id', '=', att_id), ('device_id', '=', self.id)])
                        
                        try:
                            #atten_ids = hr_attendance.search([('employee_id','=',employees.name.id), ('name','=',atten_time)])
                            #if atten_ids:
                            #    _logger.info('Attendance For Employee' + str(employees.name.name)+ 'on Same time Exist')
                            #    continue
                            #else:
                            punch_flag = lattendance.punch
                            if self.api_type == 'legacy':
                                punch_flag = lattendance.status
                            
                            if self.action == 'both':
                                if punch_flag in [0,2,4]:
                                    action = 'sign_in'
                                elif punch_flag in [1,3,5]:
                                    action = 'sign_out'

                                else:
                                    action = 'sign_none'
    #                                 if not employees.name:
    #                                     continue
    #                                 action = self.get_day_worktime(employees.name, lattendance.timestamp.strftime('%A'), lattendance.timestamp.date(), lattendance.timestamp)[0]
    #                                 if not action:
    #                                     raise UserError('Please make sure you have properly configured employee contract in order to be able to fetch attendances')
                            else:
                                action = self.action
    #                            -----------------------------------------------------------------------------
    #                            --- Skip this Check for Countries Outside UAE since holiday is not on Friday
    #                             if lattendance.timestamp.strftime('%A') == 'Friday':
    #                                 action = 'sign_none'
    #                            -----------------------------------------------------------------------------
                            if action != False:
                                if not employees.name.id:
                                    _logger.info('No Employee record found to be associated with User ID: ' + str(att_id)+ ' on Finger Print Mahcine')
                                    continue
                                atten_ids = hr_attendance.search([('employee_id','=',employees.name.id), ('name','=',atten_time)])
                                if atten_ids:
                                    _logger.info('Attendance For Employee' + str(employees.name.name)+ 'on Same time Exist')
                                    atten_ids.write({'name':atten_time,
                                                                    'employee_id':employees.name.id,
                                                                    'date':lattendance.timestamp.date(),
                                                                    'attendance_status': action,
                                                                    'day_name': lattendance.timestamp.strftime('%A')})
                                else:
                                    atten_id = hr_attendance.create({'name':atten_time,
                                                                    'employee_id':employees.name.id,
                                                                    'date':lattendance.timestamp.date(),
                                                                    'attendance_status': action,
                                                                    'day_name': lattendance.timestamp.strftime('%A')})
                                    _logger.info('Creating Draft Attendance Record: ' + str(atten_id) + 'For '+ str(employees.name.name))                                
                        except Exception as e:
                            _logger.error('Exception' + str(e))
                            #pass
                    else:
                        _logger.warn('Skip attendance because its before the threshold ' + str(curr_date))
            else:
                _logger.warn('No attendance Data to Fetch')
        except ZKNetworkError as e:
            if e.args[0] == "can't reach device (ping %s)" % self.ipaddress:
                raise Warning("can't reach device (ping %s), make sure the device is powered on and connected to the network" % self.ipaddress)
            else:
                raise Warning(e)
        except ZKErrorResponse as e:
            if e.args[0] == 'Unauthenticated':
                raise Warning("Unable to connect (Authentication Failure), Kindly supply correct password for the device.")
            else:
                raise Warning(e)
        except timeout:
            raise Warning("Connection timed out, make sure the device is turned on and not blocked by the Firewall")
        except Exception as e:
            raise Warning(e)
        finally:
            if conn:
                conn.disconnect()
        return True

    def get_day_worktime(self, employee, day_id, date, atte_datetime):
        day_of_week = {'Monday':0 ,'Tuesday':1 ,'Wednesday':2 ,'Thursday':3 ,'Friday':4 ,'Saturday':5 ,'Sunday':6 }
        contract_id = self.env['hr.payslip'].get_contract(employee, date, date)
        action = 'sign_none'
        if contract_id:
            contract = self.env['hr.contract'].browse(contract_id)
            if contract.resource_calendar_id:
                for day in contract.resource_calendar_id.attendance_ids:
                    if int(day.dayofweek) == day_of_week[day_id]:
                        time_hour = day.hour_from
                        in_out_time = self.convert_to_float(str(atte_datetime.time()))[0]
                        in_diff  = in_out_time-time_hour
                        out_diff = day.hour_to-in_out_time
                        # 5,4 range (ex : from 8AM to 1PM sign_in , from 1PM to 5PM sign_out)
                        if in_diff <= 5:
                            action = 'sign_in'
                        elif out_diff <= 4:
                            action = 'sign_out'
                        return action
        else:
            return False
        
    name = fields.Char(string='Device', required=True)
    ipaddress = fields.Char(string='IP Address', required=True)
    portnumber = fields.Integer(string='Port', required=True)
    fetch_days = fields.Integer('Attendance Fetching Limit (days)', deafult=-1)
    action = fields.Selection(selection=[('sign_in','Sign In'),('sign_out','Sign Out'),('both','All')], string='Action', default='sign_in', required=True)
    #apiversion = fields.Selection(selection=[('ZKLib', 'ZKLib'), ('SOAPpy', 'SOAPpy')], string='API', default='ZKLib', readonly=True)
    time_zone = fields.Selection('_tz_get', string='Timezone', required=True, default=lambda self: self.env.user.tz or 'UTC')
    password = fields.Char('Device Password')
    protocol = fields.Selection(selection=[('tcp', 'TCP'), ('udp', 'UDP')], string='Connection Protocol', required=True, default='tcp')
    ommit_ping = fields.Boolean(string='Ommit Ping', default=False)
    api_type = fields.Selection(selection=[('legacy', 'Legacy API'), ('new', 'New API')], string='API Type', default='new')
    
    @api.model
    def _tz_get(self):
        return [(x, x) for x in all_timezones]
    
    @api.constrains('ipaddress', 'portnumber')
    def _check_unique_constraint(self):
        self.ensure_one()
        record = self.search([('ipaddress', '=', self.ipaddress), ('portnumber', '=', self.portnumber)])
        if len(record) > 1:
            raise ValidationError('Device already exists with IP ('+str(self.ipaddress)+') and port ('+str(self.portnumber)+')!')

    def convert_to_float(self, time_att):
        h_m_s = time_att.split(":")
        hours = int(h_m_s[0])
        minutes_1 = float(h_m_s[1])/60.0
        minutes = ("%.2f" % minutes_1)
        return hours+float(minutes)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        #_logger.info('Biometric Device Info Unique constraint check')
        default = dict(default or {})
        default['name'] = _("%s (copy)") % (self.name or '')
        default['ipaddress'] = _("%s (copy)") % (self.ipaddress or '')
        default['portnumber'] = self.portnumber
        return super(BiomtericDeviceInfo, self).copy(default)
    
    
