{
    'name' : 'CustomSO',
    'version': '4.0',
    'Summary': 'Custom SO',
    'description': 'Add a Payment Method field at sale.order.line',
    'license': 'LGPL-3',
    'depends': [
        'sale_management'
    ],   
    'data': [
        'views/so_view.xml',
    ], 
    'installable': True,
    'application':True,
    'auto_install':True
}