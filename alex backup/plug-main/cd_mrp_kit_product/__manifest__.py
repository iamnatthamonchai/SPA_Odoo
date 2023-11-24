# -*- coding: utf-8 -*-
{
    'name': "Mrp Extend",

    'summary': """FOR BUNDLE LINE PRODUCT USING""",

    'description': """
        FOR BUNDLE LINE PRODUCT USING LIKE BOM LINE AND WILL HIDE MAIN MRP MENU
      
    """,

    'author': "Creative Dev",

    'website': "https://creativedev.co.th/",

    'category': 'Account',

    'version': '1.0',

    'depends': [
        'mrp',
    ],

    'data': [
        'security/mrp_user_group.xml',
        'views/mrp_menu_view.xml',
        'views/mrp_product_view.xml',
        'views/mrp_bundle_view.xml',
    ],

    'license': "LGPL-3",

    'installable': True,

    'application': False,
}