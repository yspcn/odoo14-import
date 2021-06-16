from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    x_studio_kilograms_per_unit_eg_05_for_500g = fields.Float(digits=dp.get_precision('Kilograms per unit (eg 0.5 for 500g)'))
