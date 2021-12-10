# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = "account.move"

    def _get_ordered_invoice_lines(self):
        return self.line_ids.sorted(
            key=self.env["account.move.line"]._get_section_ordering()
        ).filtered(lambda r: not r.exclude_from_invoice_tab)


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def _get_section_group(self):
        return self.mapped(self._get_section_grouping())

    @api.model
    def _get_section_grouping(self):
        invoice_section_grouping = self.env.company.invoice_section_grouping
        if invoice_section_grouping == "sale_order":
            return "sale_line_ids.order_id"
        raise UserError(_("Unrecognized invoice_section_grouping"))

    @api.model
    def _get_section_ordering(self):
        return lambda r: r.mapped(r._get_section_grouping())
