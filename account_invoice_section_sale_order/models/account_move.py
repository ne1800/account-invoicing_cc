# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    def _get_ordered_invoice_lines(self):
        return self.line_ids.sorted(
            key=self.env["account.move.line"]._get_section_ordering()
        ).filtered(lambda r: not r.exclude_from_invoice_tab)


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    @api.model
    def _get_section_grouping(self):
        return "sale_line_ids.order_id"

    @api.model
    def _get_section_ordering(self):
        return lambda r: r.mapped(r._get_section_grouping())
