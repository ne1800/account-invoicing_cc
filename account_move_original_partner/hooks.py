# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from logging import getLogger

from odoo import SUPERUSER_ID, api

_logger = getLogger(__name__)


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        force_compute_original_partners(env)


def force_compute_original_partners(env):
    """
    Force compute original partners: field is not automatically recomputed
    upon module install, so we need to force it
    """
    domain = [("move_type", "=", "out_invoice")]
    inv = env["account.move"].search(domain)
    _logger.info(f"Force-compute original partners on {len(inv)} invoices...")
    inv._compute_original_partner_ids()
