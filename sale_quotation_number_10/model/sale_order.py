
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(SaleOrder, self).copy(default)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sale.quotation') or '/'
        return super(SaleOrder, self).create(vals)

    @api.multi
    def action_confirm(self):
        if super(SaleOrder, self).action_confirm():
            for sale in self:
                quo = sale.name
                sale.write({
                    'origin': quo,
                    'name': self.env['ir.sequence'].next_by_code(
                        'sale.order')
                })
        return True
