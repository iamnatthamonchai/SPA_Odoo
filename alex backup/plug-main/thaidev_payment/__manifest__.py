# -*- coding: utf-8 -*-
{
    'name': "thaidev_payment",
    'summary': """WeCarDealor Payment Receipt""",
    'description': """WeCarDealor Payment Receipt""",
    'author': "Spellbound Soft Solutions",
    'website': "http://www.spellboundss.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','web','account','base_accounting_kit'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}