from odoo import fields, models


class CreateTrainerWizard(models.TransientModel):
    _name = 'create.trainer.wizard'
    _description = 'Create Trainer Wizard'


    name = fields.Char(string="Trainer Name", required=True, default='Coach / ')
    gym_id = fields.Many2one('gym.gym', string='Gym')
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", default='male', tracking=True)
    expertise = fields.Text(string="Expertise")
    certifications = fields.Text(string="Certifications")


    def action_trainer_member(self):
        """Create a new gym Trainer."""
        self.env['gym.trainer'].create({
            'name' : self.name,
            'gym_id' : self.gym_id.id,
            'phone' : self.phone,
            'email' : self.email,
            'gender' : self.gender,
            'expertise' : self.expertise,
            'certifications' : self.certifications,
        })


