# -*- coding: utf-8 -*-
{
    'name': 'Configurable Chatter Position',
    'version': '3.0.0',
    'category': '',
    'summary': 'Configurable Chatter Position',
    'description': 'Configurable Chatter Position',
    'sequence': '100',
    'author': 'Odoo Developers',
    'support': 'developersodoo@gmail.com',
    'depends': ['web', 'mail'],
    'demo': [],
    'data': [
        'views/res_users.xml',
        'views/web.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/od_chatter_position/static/src/scss/chatter_position.scss',
            '/od_chatter_position/static/src/scss/attachment.scss',
            '/od_chatter_position/static/src/js/form.js',
        ],
    },
    'license': 'OPL-1',
    'price': 5,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
}
