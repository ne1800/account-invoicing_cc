# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import date
from odoo.tests.common import SingleTransactionCase


class TestCrmOpportunityCurrency(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env.ref("base.res_partner_1")
        cls.contract = cls.env["ebill.payment.contract"].create(
            {
                "partner_id": cls.customer.id,
                "state": "draft",
                "date_start": "2019-05-05",
                "date_end": "2020-05-05",
            }
        )

    def test_contract_validity(self):
        self.assertFalse(self.contract.is_valid)
        self.contract.state = "open"
        self.assertTrue(self.contract.is_valid)
