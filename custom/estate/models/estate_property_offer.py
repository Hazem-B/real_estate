from datetime import date, timedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", copy=False, required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date", inverse="_inverse_date")
    create_date = fields.Date(default=date.today())

    @api.depends("create_date", "validity")
    def _compute_date(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            record.create_date = record.date_deadline - timedelta(days=record.validity)
            x = record.date_deadline - record.create_date
            record.validity = int(x.strftime('%Y%m%d'))
