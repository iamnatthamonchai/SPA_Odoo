# -*- coding: utf-8 -*-
{
    'name': "WeCarDealor Invoice",

    'summary': """WeCarDealor Custom Invoice Number 1""",

    'description': """Custom Invoice Number 1 for WeCarDealor""",

    'author': "ANDAMAN",
    'website': "http://www.billiard.co.zw",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv', 
        'views/report_invoice1.xml',
        'views/views.xml',
    ],
    'css': [
       'static/src/css/report_styles.css',
    ],
    
}
