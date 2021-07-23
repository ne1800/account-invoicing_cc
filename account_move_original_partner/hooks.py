# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        domain = [("move_type", "=", "out_invoice")]
        # Force-compute the field on existing records
        env["account.move"].search(domain)._compute_original_partner_ids()
