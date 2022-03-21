{
    'name': 'Real estate',
    'sequence': -100,
    'depends': ['base_setup', 'base'],
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/property_type_views.xml',
             'views/property_tag_views.xml',
             'views/estate_menus.xml'
             ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}