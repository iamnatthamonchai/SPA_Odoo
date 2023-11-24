# -*- coding: utf-8 -*-
{
    'name': "WeCarDealor Purchase order",
    'summary': """WeCarDealor Purchase order receipt""",
    'description': """WeCarDealor Purchase order receipt""",
    'author': "Spellbound Soft Solutions",
    'website': "http://www.spellboundss.com",
    'category': 'Operations/Purchase',
    'version': '0.1',
    'depends': ['base','web','purchase','purchase_request'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/purchase_request.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}