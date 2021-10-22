# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestAccountLineDescription(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_2 = cls.env.ref("product.product_product_2")

        consumable_cat = cls.env["product.category"].search(
            [("name", "=", "Consumable")]
        )

        cls.product_1.categ_id = consumable_cat
        cls.product_2.categ_id = consumable_cat

        cls.product_1.accounting_description = "Product1_acc_desc"

        cls.account_move = cls.env["account.move"]
        invoice_form = Form(
            cls.account_move.with_context(default_move_type="out_invoice")
        )
        invoice_form_2 = Form(
            cls.account_move.with_context(default_move_type="out_invoice")
        )

        invoice_form.partner_id = invoice_form_2.partner_id = cls.partner_1

        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = cls.product_1
            line_form.quantity = 1
            line_form.price_unit = 2.99
        cls.invoice = invoice_form.save()
        cls.invoice.action_post()

        with invoice_form_2.invoice_line_ids.new() as line_form:
            line_form.product_id = cls.product_2
            line_form.quantity = 1
            line_form.price_unit = 2.99

        cls.invoice_2 = invoice_form_2.save()
        cls.invoice_2.action_post()

    def test_invoice_line_description(self):
        inv_line_with_product = self.invoice.invoice_line_ids.filtered(
            lambda x: x.product_id
        )
        self.assertTrue(self.product_1.accounting_description)
        self.assertEqual(
            inv_line_with_product.name, self.product_1.accounting_description
        )
        self.assertEqual(
            inv_line_with_product.name, inv_line_with_product.external_name
        )

        inv_line_with_product = self.invoice_2.invoice_line_ids.filtered(
            lambda x: x.product_id
        )
        self.assertFalse(self.product_2.accounting_description)
        self.assertNotEqual(
            inv_line_with_product.name, self.product_1.accounting_description
        )
        self.assertEqual(inv_line_with_product.name, self.product_1.name)
        self.assertEqual(
            inv_line_with_product.name, inv_line_with_product.external_name
        )
