from email.policy import default

from odoo import models, fields, api, _


class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    image = fields.Binary("Image")
    birth_day = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Char(string='Address')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True)
    notes = fields.Text(string='Notes')
    gym_id = fields.Many2one('gym.gym', string='Gym')
    subscription_ids = fields.One2many('member.subscription','member_id',string='Subscription')
    health_ids = fields.One2many('member.health','member_id',string='Subscription')
    trainer_id = fields.Many2one(comodel_name='gym.trainer',string="Trainer", domain="[('gym_id', '=', gym_id)]",)
    active = fields.Boolean(string="Active", default=True)


    @api.depends('birth_day')
    def _compute_age(self):
        for record in self:
            if record.birth_day:
                today = fields.date.today()
                birth_date = record.birth_day
                record.age = today.year - birth_date.year - (
                            (today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.age = 0

    def action_draft(self):
        for rec in self:
            rec.state='draft'

    def action_active(self):
        for rec in self:
            rec.state='active'

    def action_inactive(self):
        for rec in self:
            rec.state='inactive'

    def action_cancelled(self):
        for rec in self:
            rec.state='cancelled'

class MemberHealth(models.Model):
    _name = 'member.health'
    _description = 'Member Health Details'

    member_id = fields.Many2one('gym.member', string='Member')  # العلاقة مع العضو
    weight = fields.Float(string="Weight (kg)", required=True)
    height = fields.Float(string="Height (m)", required=True)
    bmi = fields.Float(string="BMI", compute="_compute_bmi", store=True)
    health_status = fields.Selection([
        ('good', 'Good'),
        ('average', 'Average'),
        ('needs_attention', 'Needs Attention')
    ], string="Health Status", compute="_compute_health_status", store=True)
    notes = fields.Text(string='Notes')

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        for record in self:
            if record.weight > 0 and record.height > 0:
                record.bmi = record.weight / (record.height ** 2)
            else:
                record.bmi = 0  # إذا كانت القيم غير صالحة، يتم وضع 0

    @api.depends('bmi')
    def _compute_health_status(self):
        for record in self:
            if record.bmi < 18.5:
                record.health_status = 'needs_attention'  # الوزن أقل من الطبيعي
            elif 18.5 <= record.bmi <= 24.9:
                record.health_status = 'good'  # الوزن مثالي
            elif 25 <= record.bmi <= 29.9:
                record.health_status = 'average'  # الوزن زائد قليلًا
            else:
                record.health_status = 'needs_attention'  # السمنة

class MemberSubscription(models.Model):
    _name = 'member.subscription'
    _description = 'Member Subscription Details'

    member_id = fields.Many2one('gym.member', string='Member')
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    duration = fields.Integer(string="Duration (days)", compute="_compute_duration", store=True)
    subscription_type = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('semi_annual', 'Semi-Annual'),
        ('yearly', 'yearly')
    ], string="Subscription Type", required=True, default='monthly')
    subscription_fee = fields.Float(string="Subscription Fee", required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], string="Subscription Status", default='active')
    auto_renewal = fields.Boolean(string="Auto Renewal", default=False)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days

    @api.depends('start_date', 'subscription_type')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.subscription_type:
                if record.subscription_type == 'daily':
                    record.end_date = fields.Date.add(record.start_date, days=1)
                elif record.subscription_type == 'monthly':
                    record.end_date = fields.Date.add(record.start_date, months=1)
                elif record.subscription_type == 'semi_annual':
                    record.end_date = fields.Date.add(record.start_date, months=6)
                elif record.subscription_type == 'yearly':
                    record.end_date = fields.Date.add(record.start_date, months=12)




