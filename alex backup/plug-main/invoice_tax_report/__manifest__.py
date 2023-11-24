# -*- coding: utf-8 -*-
{
    'name': "Invoice Tax Report",
    'summary': """Invoice Tax Report""",
    'description': """Invoice Tax Report""",
    'author': "Spellbound Soft Solution",
    'website': "http://www.spellboundss.com",
    'category': 'Account',
    'version': '13.0.1',
    'depends': ['base','account','web'],
    'data': [
        'report/paper_format.xml',
        'report/report_invoice.xml',
        'report/report_invoice_tax.xml',
        'report/report_invoice_tax_continue.xml',
        'views/account_inv.xml',
    ],
}
