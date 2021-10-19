# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SavepointCase


class TestInvoiceGroupBySaleOrder(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_2 = cls.env.ref("product.product_product_2")
        cls.product_2.invoice_policy = "order"

        cls.product_1.accounting_description = "Product1_acc_desc"
        cls.product_1.invoice_policy = "order"
        cls.order1_p1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "partner_shipping_id": cls.partner_1.id,
                "partner_invoice_id": cls.partner_1.id,
                "client_order_ref": "ref123",
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                            "price_unit": 20,
                            "product_uom_qty": 1,
                            "product_uom": cls.product_1.uom_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                            "price_unit": 20,
                            "product_uom_qty": 1,
                            "product_uom": cls.product_1.uom_id.id,
                        },
                    ),
                ],
            }
        )
        cls.order1_p1.action_confirm()

        cls.order2_p1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "partner_shipping_id": cls.partner_1.id,
                "partner_invoice_id": cls.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_2.id,
                            "price_unit": 20,
                            "product_uom_qty": 1,
                            "product_uom": cls.product_2.uom_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_2.id,
                            "price_unit": 20,
                            "product_uom_qty": 1,
                            "product_uom": cls.product_2.uom_id.id,
                        },
                    ),
                ],
            }
        )
        cls.order2_p1.action_confirm()

    def test_invoice_line_name(self):

        # For 1st SO check invoice line is same as product description
        invoice_id = self.order1_p1._create_invoices()
        lines = invoice_id[0].line_ids.filtered(
            lambda r: not r.exclude_from_invoice_tab
        )

        for line in lines:
            self.assertEqual(line.name, self.product_1.accounting_description)
            self.assertEqual(line.external_name, self.product_1.name)

        # For 2nd SO make sure invoice line name isn't set to product description

        invoice_id = self.order2_p1._create_invoices()
        lines = invoice_id[0].line_ids.filtered(
            lambda r: not r.exclude_from_invoice_tab
        )

        for line in lines:
            self.assertNotEqual(line.name, self.product_2.accounting_description)
            self.assertEqual(line.name, self.product_2.name)
            self.assertEqual(line.external_name, line.name)