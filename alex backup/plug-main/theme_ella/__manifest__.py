# -*- coding: utf-8 -*-

{
    'name': 'Theme Ella',
    'category': 'Theme/Ecommerce',
    'summary': """Multipurpose Premium Responsive Odoo Theme - Fashion, Furniture, Sports, Jewellery, Corporate""",
    'version': '1.3',
    'sequence': 1000,
    'author': 'Atharva System',
    'license' : 'OPL-1',
    'support': 'support@atharvasystem.com',
    'website' : 'https://www.atharvasystem.com',
    'description': """
    Theme Ella is one of the most powerful, amazing and flexible theme on Odoo store. 
    Multipurpose Premium Responsive Odoo Themes - Fashion, Furniture, Sports, Jewellery, Corporate.
Creative theme,
Ecommerce theme,
Entertainment theme,
Personal theme,
Services theme,
Technology theme,
Business theme,
Multipurpose odoo theme,
Multi-purpose theme,
Theme Ella, 
Odoo new themes,
Ella Theme, 
Bootstrap4 odoo themes,
eCommerce Businesses,
Odoo RTL Theme,
Right to left theme
        """,
    'depends': ['website_theme_install','atharva_theme_general'],
    'data': [
        'views/customize_theme_templates.xml',
        'views/assets.xml',
        'views/snippets.xml',
    ],
    'live_test_url': 'http://theme-ella.atharvasystem.com/',
    'images': ['static/description/ella_banner.png','static/description/ella_banner_screenshot.png'],
    'price': 78.00,
    'currency': 'EUR',
    'application': True,
}
