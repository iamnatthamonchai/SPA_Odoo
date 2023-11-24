# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'All In One Cancel Sales,Purchases and Delivery,Invoice',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Sales',
    'maintainer': 'Craftsync Technologies',
    'summary': """ all in one cancel  ALL IN ONE CANCEL   
    """,

    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['purchase_stock','sale_management','sale_stock'],
    'data': [

        'views/res_config_settings_views.xml',
        'views/view_purchase_order.xml',
        'views/stock_warehouse.xml',
        'views/view_sale_order.xml',
        'views/stock_picking.xml',
        'wizard/view_cancel_invoice_wizard.xml',
        'views/invoice.xml',
        'wizard/view_cancel_delivery_wizard.xml',

    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 34.99,
    'currency': 'EUR',

    'images': ['static/description/main_screen.png'],

}
