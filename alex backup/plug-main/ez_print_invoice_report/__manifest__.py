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
    'depends' : ['sale','base'],
    "support": "support@creatiedev.asia",
    'data' : [
        # 'views/res_company.xml',
        # 'views/show_discount_amount.xml',
        'report/report_asset.xml',
        'report/report_reg.xml',
        'report/invoice_and_tax_invoice_report.xml',
        'report/invoice_report.xml',
        'report/tax_invoice_report.xml',
        'report/tax_invoice_and_receipt_report.xml',
        'report/creditnote_report.xml',
        'report/debitnote_report.xml',
        # 'wizard/creditor_report_view.xml',
        # 'wizard/receivable_report_view.xml',

        #################This is example for DOT ######
        # 'report/invoice_receipt_dot.xml',
    ],


    'qweb': [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
