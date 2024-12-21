{
    'name': 'Gym Management',
    'version': '17.1.0',
    'summary': 'Manage gym memberships, trainers, schedules, and payments',
    'description': """
        Gym Management System
        =====================
        This module allows you to manage gym memberships, trainers, schedules, and payments.
        Features:
        - Member registration
        - Membership plans
        - Trainer allocation
        - Class schedules
        - Payment tracking
        - Reports
    """,
    'category': 'Management',
    'author': 'Arafa',
    'website': 'http://www.yourwebsite.com',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',

        'views/gym_view.xml',
        'views/member_view.xml',
        'views/trainer_view.xml',

        'report/gym_member_report.xml',
        'report/gym_report.xml',
        'report/gym_trainer_report.xml',

        'wizard/create_member_wizard_view.xml',
        'wizard/create_trainer_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
