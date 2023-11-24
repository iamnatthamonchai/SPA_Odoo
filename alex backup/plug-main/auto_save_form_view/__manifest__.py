{
    'name': 'Auto Save Form View',
    'summary': 'The Form View will be saved automatically at a particular time, avoid losing your data.',
    'description': 'The Form View will be saved automatically at a particular time, avoid losing your data. ',
    'author': "Sonny Huynh",
    'category': 'Extra Tools',
    'version': '0.1',
    'depends': ["base", "base_setup"],
    'data': [
        'data/auto_save_data.xml',
        'views/res_config_settings_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'auto_save_form_view/static/src/js/worker_save.js',
            'auto_save_form_view/static/src/js/auto_save_form_view.js',
        ],
    },

    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 45.00,
    'currency': 'EUR',
}