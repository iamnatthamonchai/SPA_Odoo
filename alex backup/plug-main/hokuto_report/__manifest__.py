# -*- coding: utf-8 -*-
{
    'name': 'SO Report Hokuto Style',
    'version': '13.0.0.2',
    'summary': 'Create And Manage Report',
    'description': """
        1.  Create and manage Report
    """,
    'license': 'AGPL-3',
    'author': 'Zoomsaccount',
    'website': 'www.zoomsacc.com',
    'sequence': 3,
    'depends': ['base', 'sale_management'],
    'data': [
        'report/report_sale_order_inherit.xml',
        'report/sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
