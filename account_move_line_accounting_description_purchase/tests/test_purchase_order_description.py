# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields
from odoo.tests.common import SavepointCase


class TestPurchaseOrderDescription(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_2 = cls.env.ref("product.product_product_2")
        cls.product_2.invoice_policy = "order"

        cls.product_1.accounting_description = "Product1_acc_desc"
        cls.product_1.invoice_policy = "order"

        cls.po_1 = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                            "product_qty": 5.0,
                            "product_uom": cls.product_1.uom_id.id,
                            "price_unit": 10,
                            "date_planned": fields.Datetime.now(),
                        },
                    )
                ],
            }
        )
        cls.po_1_line = cls.po_1.order_line
        cls.po_1.button_confirm()
        cls.po_1.button_approve()

        cls.po_2 = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_2.id,
                            "product_qty": 5.0,
                            "product_uom": cls.product_2.uom_id.id,
                            "price_unit": 10,
                            "date_planned": fields.Datetime.now(),
                        },
                    )
                ],
            }
        )
        cls.po_2_line = cls.po_2.order_line
        cls.po_2.button_confirm()
        cls.po_2.button_approve()

    def test_purchase_order_line_name(self):

        # For 1st PO check order line is same as product description

        self.assertEqual(self.po_1_line.name, self.product_1.accounting_description)
        self.assertEqual(self.po_1_line.external_name, self.product_1.name)

        # For 2nd PO make sure line name isn't set to product description

        self.assertFalse(self.product_2.accounting_description)
        self.assertNotEqual(self.po_2_line.name, self.product_2.accounting_description)
        self.assertEqual(self.po_2_line.name, self.product_2.name)
        self.assertEqual(self.po_2_line.external_name, self.po_2_line.name)
