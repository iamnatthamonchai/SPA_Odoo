# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
{
    'name'       : 'Purchase Multi Location',
    'version'    : '15.0',
    "author"     : "DP InfoSOl",
    "support"    : "help.dpinfosol@gmail.com",
    'category'   : 'Mail',
    'summary'    : '''Add functionality to set explicit destination location in purchase order lines.''',
    'description': """This module allows you to set destination location in purchase order lines.
Multi location in purchase order
purchase order line multi location
location in purchase order
purchase order by location
purchase order line by locations
putaway from purchase order
purchase location
order by location
transfer goods to specific location
location transfer goods
purchase transfer goods
    """,
    'depends'    : ['purchase_stock'],
    'data'       : [
                    'views/purchase_order_view.xml',
                    ],
    'installable' : True,
    'auto_install': False,
    'price'       : 10,
    'currency'    : "EUR",
    'images'      : ["static/description/banner.png",],
}
