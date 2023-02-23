# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceMerge(AccountTestInvoicingCommon):
    """
    Tests for Account Invoice Merge.
    """

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.company = cls.company_data_2["company"]
        invoice_date = fields.Date.today()
        cls.invoice1 = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_a,
            invoice_date=invoice_date,
            products=cls.product_a,
        )
        cls.now = cls.invoice1.create_date
        cls.invoice2 = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_a,
            invoice_date=invoice_date,
            products=cls.product_a,
        )
        cls.invoice3 = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_b,
            invoice_date=invoice_date,
            products=cls.product_a,
        )
        cls.invoice4 = cls.init_invoice(
            "in_invoice",
            partner=cls.partner_a,
            invoice_date=invoice_date,
            products=cls.product_a,
        )
        cls.invoice5 = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_a,
            invoice_date=invoice_date,
            products=cls.product_a,
        )
        cls.invoice6 = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_a,
            products=cls.product_a,
            invoice_date=invoice_date,
            company=cls.company,
        )

    def setUp(self):
        super(TestAccountInvoiceMerge, self).setUp()
        self.company_model = self.env["res.company"]
        self.par_model = self.env["res.partner"]
        self.context = self.env["res.users"].context_get()
        self.acc_model = self.env["account.account"]
        self.inv_model = self.env["account.move"]
        self.journal_model = self.env["account.journal"]
        self.inv_line_model = self.env["account.move.line"]
        self.wiz = self.env["invoice.merge"]

    def _get_wizard(self, active_ids, create=False):
        wiz = self.wiz.with_context(
            active_ids=active_ids,
            active_model="account.move",
        )
        if create:
            wiz = wiz.create({})
        return wiz

    def test_invoice_merge(self):

        self.assertEqual(len(self.invoice1.invoice_line_ids), 1)
        self.assertEqual(len(self.invoice2.invoice_line_ids), 1)
        invoice_len_args = [
            ("create_date", ">=", self.now),
            ("partner_id", "=", self.partner_a.id),
            ("state", "=", "draft"),
        ]
        start_inv = self.inv_model.search(invoice_len_args)
        self.assertEqual(len(start_inv), 5)

        wiz = self._get_wizard([self.invoice1.id, self.invoice2.id], create=True)
        action = wiz.merge_invoices()

        self.assertLessEqual(
            {
                "type": "ir.actions.act_window",
                "binding_view_types": "list,form",
                "xml_id": "account.action_move_out_invoice_type",
            }.items(),
            action.items(),
            "There was an error and the two invoices were not merged.",
        )

        end_inv = self.inv_model.search(invoice_len_args)
        self.assertEqual(len(end_inv), 4)
        self.assertEqual(len(end_inv[0].invoice_line_ids), 1)
        self.assertEqual(end_inv[0].invoice_line_ids[0].quantity, 2.0)

    def test_error_check(self):
        """Check"""
        # Different partner
        wiz = self._get_wizard([self.invoice1.id, self.invoice3.id], create=True)
        self.assertEqual(
            wiz.error_message, "All invoices must have the same: \n- Partner"
        )

        # Check with only one invoice
        wiz = self._get_wizard([self.invoice1.id], create=True)
        self.assertEqual(
            wiz.error_message,
            "Please select multiple invoices to merge in the list view.",
        )

        # Check with two different invoice type
        wiz = self._get_wizard([self.invoice1.id, self.invoice4.id], create=True)
        self.assertEqual(
            wiz.error_message, "All invoices must have the same: \n- Type\n- Journal"
        )

        # Check with a canceled invoice
        self.invoice5.button_cancel()
        wiz = self._get_wizard([self.invoice1.id, self.invoice5.id], create=True)
        self.assertEqual(
            wiz.error_message,
            "All invoices must have the same: \n- Merge-able State (ex : Draft)",
        )

        # Check with another company
        wiz = self._get_wizard([self.invoice1.id, self.invoice6.id], create=True)
        self.assertEqual(
            wiz.error_message, "All invoices must have the same: \n- Journal\n- Company"
        )
