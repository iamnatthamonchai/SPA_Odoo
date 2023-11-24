# -*- coding: utf-8 -*-
{
    'name': "Sale Order Type",

    'summary': """
        Sale Order Type""",

    'description': """
        This module adds a typology for the sales orders. In each different type, you can define, invoicing and refunding journal, a warehouse, a sequence, the shipping policy, the invoicing policy, a payment term, a pricelist and an incoterm.
        You can see sale types as lines of business.
        You are able to select a sales order type by partner so that when you add a partner to a sales order it will get the related info to it.
    """,

    'author': "safecoms,naing.lynnhtun@safecoms.com",
    'website': "https://www.safecoms.co.th",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales Management',
    'version': '0.2',
    'license': "AGPL-3",

    # any module necessary for this one to work correctly
    "depends": [
        'sale_stock',
        'sale_management',
        'purchase',
        'purchase_stock',
        'sale_purchase_inter_company_rules',
        'mrp_plm',
        'stock',
        'sale_mrp',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/sale_order_type_view.xml",
        "data/default_type.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}