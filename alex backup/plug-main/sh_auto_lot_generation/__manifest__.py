# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    "name" : "Auto Generate Lot Number in Incoming Shipment",
    "author" : "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",    
    "category": "Warehouse",
    "summary": "Auto Lot Generate Automatic Lot Assign Auto Assign Lot Selection Auto Generate Lot In Picking Automation Lot Generation Create Auto Lot Based On Prefix Auto Generate Lot In Picking Clear Lot Custom Lot Number Based On Vehicle Odoo",
    "description": """This module auto generates lot numbers for receipts. Just select "By Lots" in tracking and enter prefix number in receipt then click "Assign Lot Numbers". So it generates lot number based on lot quantity and prefix number.""", 
    "version": "15.0.1",
    "depends": ["stock"],
    "data": [
        
        'data/ir_sequence_data.xml',
        'views/stock.xml',

    ],
    "auto_install": False,
    "installable": True,
    "application": True,
    "images": ["static/description/background.png",],
    "license": "OPL-1",
    "price": 20,
    "currency": "EUR"  
}
