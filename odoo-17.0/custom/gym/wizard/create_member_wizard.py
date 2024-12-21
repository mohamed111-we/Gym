from odoo import fields, models


class CreateMemberWizard(models.TransientModel):
    _name = 'create.member.wizard'
    _description = 'Create Member Wizard'

    name = fields.Char(string='Name', required=True)
    gym_id = fields.Many2one('gym.gym', string='Gym')
    trainer_id = fields.Many2one(comodel_name='gym.trainer', string="Trainer", )
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Char(string='Address')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male', tracking=True)
    notes = fields.Text(string='Notes')

    def action_create_member(self):
        """Create a new gym member."""
        self.env['gym.member'].create({
            'name': self.name,
            'gym_id': self.gym_id.id,
            'trainer_id': self.trainer_id.id,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'gender': self.gender,
            'notes': self.notes,
        })
