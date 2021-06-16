# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def sh_import_journal_item(self):
        if self:
            action = self.env.ref(
                'sh_import_journal_item.sh_import_journal_item_action').read()[0]
            return action
