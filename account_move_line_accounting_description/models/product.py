from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    accounting_description = fields.Text(string="Accounting description")
