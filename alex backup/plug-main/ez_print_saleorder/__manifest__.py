# -*- coding: utf-8 -*-

# Part of ZOOMSACCOUNT (www.odoothaidev.com)
#
#
#                                    (((((((((((                                 
#      &&&&&&&&&&  *&&&&&&&&&&    (((         ((((  &&&       &&&,  #&&&&&&&&     
#           &&&   &&&       &&&  (((           (((( &&&&&   &&&&&,  &&&&          
#         &&&%    &&&        &&& (((            ((( &&&&&& &&& &&,     &&&&&&     
#       &&&&       &&&     &&&&  (((           (((  &&&  &&&   &&,  &&     &&&    
#      &&&&&&&&&&&   &&&&&&&&     .((((     *((((   &&&        &&,   &&&&&&&&     
#                               (((  *((((((((                                    
#                            ((((                                                 
#                         (((((        
#                       (((((   

# EZ Sale Order Form

{
    'name' : 'Thailand Print Sales Report',
    'version' : '14',
    'price' : '59.99',
    'currency': 'USD',
    'category': 'Sales Report',
    'summary' : 'Print Sales Report',
    'description': """
                Quotations and Sales Order Report:
Tags: 
Stock report
            """,
    'author' : 'CreativeDEV',
    'website' : 'https://creativedev.asia/',
    'depends' : ['sale','base','l10n_th_partner'],
    "support": "support@creatiedev.asia",
    'data' : [
        'data/assets.xml',
        'views/res_partner.xml',
        'report/report_reg.xml',
        'report/quotation_report.xml',
        'report/quotation_report_layout.xml',
        'report/quotation_report_mj.xml',
    ],
    
    'assets': {
        'web.report_assets_common': [
            "/ez_print_saleorder/static/src/css/report.css",
        ],
    },


    'qweb': [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": [ "static/description/banner.png" ],
    "license": "OPL-1",
}
