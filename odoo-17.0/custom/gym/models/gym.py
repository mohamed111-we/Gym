from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GymManagement(models.Model):
    _name = 'gym.gym'
    _description = 'Gym Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    owner_id = fields.Many2one('res.partner', string='Owner', required=True)
    phone_owner = fields.Char(related='owner_id.phone', string='Phone', store=True, readonly=True)
    email_owner = fields.Char(related='owner_id.email', string='Email', store=True, readonly=True)
    name = fields.Char(string='Gym Name', required=True)
    phone = fields.Char(string='Phone',)
    email = fields.Char(string='Email',)
    state = fields.Selection([
        ('draft', 'Draft'),    #يتم إعداد تفاصيل الجيم أو تسجيله حديثًا، ولم يتم تشغيله بعد.
        ('open', 'Open'),      # الجيم قيد التشغيل ويستقبل الأعضاء.
        ('closed', 'Closed'),  #  الجيم مغلق بشكل مؤقت (لإجازة، صيانة، أو أي سبب آخر).
        ('inactive', 'Inactive'), #الجيم مغلق بشكل دائم أو لم يعد يقدم خدماته.
    ], string='state', default='draft', tracking=True)
    location = fields.Char(string='Location')
    rating = fields.Float(string="Rating", digits=(2, 1), default=0.0)
    zip_code = fields.Char(string='Zip Code')
    description = fields.Text(string='Description')
    image = fields.Binary(string="Image")
    active = fields.Boolean(default=True)
    member_ids = fields.One2many('gym.member','gym_id',String='Member')
    trainer_ids = fields.One2many('gym.trainer','gym_id',String='Member')
    # عداد الاعضاء
    member_count = fields.Integer(string="Member Count",compute='_compute_member_count',store=True)
    # عداد المدربين
    trainer_count = fields.Integer(string="Trainer Count",compute='_compute_trainer_count',store=True)

    @api.depends('member_ids')
    def _compute_member_count(self):
        for record in self:
            record.member_count = len(record.member_ids)

    @api.depends('trainer_ids')
    def _compute_trainer_count(self):
        for record in self:
            record.trainer_count = len(record.trainer_ids)

    api.constrains('rating')
    def _check_rating(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 5:
                raise ValidationError("Rating must be between 0 and 5.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('gym.gym') or _('New')
        return super(GymManagement, self).create(vals_list)

    def action_draft(self):
        for rec in self:
            rec.state='draft'

    def action_open(self):
        for rec in self:
            rec.state='open'

    def action_closed(self):
        for rec in self:
            rec.state='closed'

    def action_inactive(self):
        for rec in self:
            rec.state='inactive'

    def action_view_member(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Members'),
            'res_model': 'gym.member',
            'view_mode': 'tree,form',
            'domain': [('gym_id', '=', self.id)],
        }

    def action_view_trainer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Members'),
            'res_model': 'gym.trainer',
            'view_mode': 'tree,form',
            'domain': [('gym_id', '=', self.id)],
        }

    def action_open_create_member_wizard(self):
        """Open the wizard for creating a new member."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create New Member'),
            'res_model': 'create.member.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_gym_id': self.id},
        }



    def action_open_create_trainer_wizard(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : _('Create New Trainer'),
            'res_model' : 'create.trainer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_gym_id': self.id},
        }

