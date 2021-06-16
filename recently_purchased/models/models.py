# -*- coding: utf-8 -*-

from odoo import models, fields, api


class recently_purchased(models.Model):
    _name = 'recently_purchased.recently_purchased'
    _description = 'recently_purchased.recently_purchased'

    name = fields.Char()
    value = fields.Integer()


