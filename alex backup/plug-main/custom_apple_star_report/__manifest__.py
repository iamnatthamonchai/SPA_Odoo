# -*- coding: utf-8 -*-
{
    'name': 'Custom Apple Star Report',
    'version': '15.0.0.0.1',
    'summary': 'Custom Apple Star Report Quotation/Invoice',
    'description': """Custom Apple Star Report Quotation/Invoice""",
    'category': 'Report',
    'author': 'Apple Star',
    'maintainer': 'AppleStar',
    'website': 'http://applestar.co.th/odoo',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'account',
        'abs_total_discount_so',
        'abs_total_discount_invoice',
    ],
    'data': [
      'data/report_paper.xml',
      'reports/template.xml',
      'reports/quotation_template_apple_star.xml',
      'reports/invoice_template_apple_star.xml',
      'reports/report.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'custom_apple_star_report/static/less/fonts.less',
            ],
        },
    'installable': True,
    'application': True,
    'auto_install': False,
}
