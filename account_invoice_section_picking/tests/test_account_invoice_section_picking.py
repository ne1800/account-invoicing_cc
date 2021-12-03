# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests.common import Form, SavepointCase


class TestAccountInvoiceSectionPicking(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.invoice_section_grouping = "delivery_picking"
        cls.partner_1 = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_delivery_01")
        cls.product_1.invoice_policy = "order"
        cls.order_1 = cls._create_order()
        cls.order_2 = cls._create_order(order_line_name=cls.product_1.name)
        cls.order_1.action_confirm()
        cls.order_2.action_confirm()

    @classmethod
    def _create_order(cls, order_line_name=None):
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner_1
        with order_form:
            with order_form.order_line.new() as line_form:
                line_form.product_id = cls.product_1
                if order_line_name is not None:
                    line_form.name = order_line_name
        return order_form.save()

    def test_group_by_delivery_picking(self):
        invoice = (self.order_1 + self.order_2)._create_invoices()
        self.assertEqual(len(invoice), 1)
        result = {
            10: (self.order_1.picking_ids.name, "line_section"),
            20: (self.order_1.order_line.name, False),
            30: (self.order_2.picking_ids.name, "line_section"),
            40: (self.order_2.order_line.name, False),
        }
        for line in invoice.line_ids.filtered(
            lambda l: not l.exclude_from_invoice_tab
        ).sorted("sequence"):
            self.assertEqual(line.name, result[line.sequence][0])
            self.assertEqual(line.display_type, result[line.sequence][1])

    # TODO: add test with warehouse using multiple delivery steps to ensure
    #  it's the delivery picking name that is printed

    # TODO: add test with product using delivered quantities after creation of
    #  a backorder
    #  - Handle possible issue with sale order line having part of its qty on
    #    first delivery and other part in backorder(s)
