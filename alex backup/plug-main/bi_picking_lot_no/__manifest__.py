# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Auto Generate Lot/Serial Number in Inventory',
    'version': '15.0.0.0',
    'category': 'Warehouse',
    'summary': 'Auto Generate lot in inventory auto serial number generate serial in inventory automation lot generation auto lot number from Picking create auto lot auto lot creation auto serial auto lot create auto generate lot number from inventory auto serial number',
    'description': """ 

        Auto Generate Lot Number in Inventory in odoo,
        Generate lot number based from Inventory,
        Shipment Auto Generate lot number from Inventory,
        picking Auto Generate lot number from incoming shipment,
        picking Automatic Generate lot number from Inventory,
        shipment Automatic Generate lot number from incoming shipment,
        auto generate lot from picking auto generate lot number from inventory,

    """,
    'author': 'BrowseInfo',
    "price": 19,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.in',
    'depends': ['base','purchase','stock','account','purchase_stock','stock'],
    'data': [
			'views/inherited_stock_picking_views.xml',
			'views/inherited_res_config_view.xml'
             ],
    'demo': [],
    'css': [],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/kkEba7D1fdk',
    "images": ['static/description/Banner.png'],
}
