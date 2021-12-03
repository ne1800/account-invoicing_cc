# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    @api.model
    def _get_section_grouping(self):
        invoice_section_grouping = self.env.company.invoice_section_grouping
        if invoice_section_grouping == "delivery_picking":
            return "sale_line_ids.move_ids.picking_id"
        return super()._get_section_grouping()
