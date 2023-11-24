# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Auto Generate serial/lot number from Picking in Odoo',
    'version': '13.0.0.2',
    'category': 'purchase',
    'sequence': 15,
    'author': 'BrowseInfo',
    'summary': 'Automatic lot number Generate from picking auto serial number generate from picking automation lot generation auto lot number from Picking create auto lot from picking create auto serial from picking auto lot creation auto serial creation auto lot create',
    'description': """ Generate serial/lot number based from MO
    Shipment Auto Generate serial number from picking order
    picking Auto Generate lot number from incoming shipment
    picking Automatic Generate serial number from picking
    shipment Automatic Generate lot number from incoming shipment
    auto generate lot from picking auto generate serial number from picking

   

    """,
    'website': 'http://www.browseinfo.in',
    'depends': ['base','purchase','stock','account','purchase_stock'],
    'data': [
            
            'views/inherited_res_config_view.xml',
            'views/inherited_stock_picking_views.xml',
             ],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 19,
    "currency": 'EUR',
    "live_test_url":'https://youtu.be/_pOYrJyIg-s',
    "images":['static/description/Banner.png'],
}
