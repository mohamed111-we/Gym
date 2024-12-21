from odoo import models, fields, api, _

class GymTrainer(models.Model):
    _name = 'gym.trainer'
    _description = 'Gym Trainer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Trainer Name", required=True, default='Coach / ')
    image = fields.Binary("Image")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    birth_day = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", default='male', tracking=True)
    expertise = fields.Text(string="Expertise")
    certifications = fields.Text(string="Certifications")
    gym_id = fields.Many2one('gym.gym', string='Gym')
    member_ids = fields.One2many(comodel_name='gym.member',inverse_name='trainer_id',string="Members")


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




