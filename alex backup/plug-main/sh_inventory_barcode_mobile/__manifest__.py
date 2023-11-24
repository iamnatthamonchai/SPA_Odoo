# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name":
    "Inventory Mobile Barcode Scanner | Inventory Mobile QRCode Scanner",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "15.0.3",
    "category": "Warehouse",
    "summary":
    "Scan Mobile Barcode, Scan Tablet Barcode App, Scan Mobile Barcode Product, Scan Product Internal Reference No, Inventory Barcode Scanner,Inventory QRCode Scanner, Stock Mobile Barcode Scanner, Stock Mobile QRCode Scanner Odoo",
    "description":
    """Do you want to scan Barcode or QRCode in your mobile? Do your time wasting in stock picking operations by manual product selection ? So here is the solutions this modules useful do quick operations of stock picking mobile Barcode or QRCode scanner. You no need to select product and do one by one. scan it and you done! So be very quick in all operations of odoo in mobile and cheers!

 Inventory Mobile Barcode Scanner Odoo
 Scan Barcode On Mobile, Scan Barcode In Tablet, Scan Product By Mobile Barcode, Scan Product By Internal Reference Number In Mobile, Scan Inventory With Mobile Barcode, Scan Stock With Mobile Barcode, Scan Stock Product With Mobile Barcode, Scan Warehouse Product With Mobile Barcode Odoo.
 Scan Mobile Barcode, Scan Tablet Barcode App, Scan Mobile Barcode Product, Scan Product Internal Reference No, Scan Mobile Barcode Inventory, Scan Mobile Barcode Stock, Scan Mobile Barcode Stock Product, Scan Mobile Barcode Product Inventory Odoo.""",
    "depends": ["stock", "sh_product_qrcode_generator"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/stock_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            'sh_inventory_barcode_mobile/static/src/scss/custom.scss',
            'sh_inventory_barcode_mobile/static/src/js/bus_notification.js',
            'sh_inventory_barcode_mobile/static/src/js/ZXing.js'
        ]
    },
    "images": [
        "static/description/background.png",
    ],
    "live_test_url": "https://youtu.be/rYUD3EyR1gk",
    "installable": True,
    "application": True,
    "autoinstall": False,
    "price": 60,
    "currency": "EUR",
    "license": "OPL-1"
}
