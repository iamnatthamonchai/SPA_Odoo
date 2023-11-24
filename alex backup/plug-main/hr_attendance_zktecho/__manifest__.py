
# -*- coding: utf-8 -*-
{
    'name': "HR Attendance ZKTeco",

    'summary': """
    Integration with ZKTeco Biometric Devices
         """,

    'description': """
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Human Resources',
    'version': '15.0.0.1',
    'license': 'LGPL-3',
    'App origin':"Base",


    'depends': ['base', 'hr', 'hr_payroll', 'hr_contract', 'hr_attendance', 'mail', 'resource'],

    'data': [
        'data/get_attendance.xml',
        'security/biometricdevice_security.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/hr_attendance_view.xml',
        'views/biometricdevice_view.xml',
        'views/hr_extensionview.xml',
        'wizard/move_attendance_wizard_view.xml',
        'wizard/generate_missing_attendance.xml',
    ],
}

