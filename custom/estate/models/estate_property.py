from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"

    title = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=today() + relativedelta(months=3), string="Availability From")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('cancelled', 'Cancelled')],
                             default='new')
    salesman_id = fields.Many2one('res.users', string="Salesman", index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total")
    best_offer = fields.Integer(string="Best Offer", compute="_compute_best_offer")

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'))
