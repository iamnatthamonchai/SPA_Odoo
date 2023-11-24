# -*- coding: utf-8 -*-
{
    'name': "DMS RV PV Report",
    'summary': """WeCarDealor RV PV Report""",
    'description': """WeCarDealor RV PV Report
    Maintained by Bill Made www.regious.co.zw""",
    'author': "Spellbound Soft Solutions",
    'website': "www.smartdms.asia",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','web','account','base_accounting_kit'],
    'data': [
        'data/report_paper_format.xml',
        # 'report/report_asset.xml',
        'report/rv_pv_report.xml',
        # 'views/views.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'dms_rv_pv_report/static/src/less/report.less',
        ],
    }
}