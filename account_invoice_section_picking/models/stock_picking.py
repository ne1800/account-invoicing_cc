# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models
from odoo.tools.safe_eval import safe_eval, time


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def _get_invoice_section_name(self):
        """Returns the text for the section name."""
        self.ensure_one()
        naming_scheme = (
            self.partner_id.invoice_section_name_scheme
            or self.company_id.invoice_section_name_scheme
        )
        if naming_scheme:
            return safe_eval(naming_scheme, {"object": self, "time": time})
        else:
            return self.name
