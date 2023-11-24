# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

{
    'name': 'Website Product Limit',
    'version': '15.0.0',
    'category': 'General',
    'license': 'LGPL-3',
    'description': '''This module provides the functionality to restrict product sale limit in webshop. Per order quantity of single product 
                      can be set and restricted using this module. Limit Quantity restrict quantity maximum quantity''',
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'http://www.sprintit.fi',
    'depends': [
      'website_sale',
    ],
    'data': [
      'view/product.xml',
      'view/website_sale_product.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sprintit_website_product_limit/static/src/js/**/*',
        ],
    },
    'demo': [
    ],
    'test': [
    ],
    'images': ['static/description/cover.jpg',],
    'installable': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',     
}
