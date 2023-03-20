# Copyright 2023 Christopher Hansen (Raumschmiede GmbH)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    ignore_invoice_auto_mail_payment_state_check = fields.Boolean(
        "Ignore Invoice Auto Mail Payment State Check",
    )


class ConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ignore_invoice_auto_mail_payment_state_check = fields.Boolean(
        related="company_id.ignore_invoice_auto_mail_payment_state_check",
        readonly=False,
    )
