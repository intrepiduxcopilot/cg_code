# -*- coding: utf-8 -*-
{
	'name': 'HELPDESK SH Dashboard Ninja',

	'summary': """
        HELPDESK dashboard SH
""",

	'description': """

""",

	'author': 'David Contreras',

	'license': 'OPL-1',

	'category': 'Tools',

	'version': '15.0.1.0.3',

	'images': ['static/description/ks_crm_ninja_banner.jpg'],

	'depends': ['ks_dashboard_ninja', 'sh_all_in_one_helpdesk'],

	'data': [
		'data/cg_helpdesk_data.xml',
	 	'data/helpdesk.stages.csv',
		'data/helpdesk.ticket.type.csv',
		'data/helpdesk.category.csv',
		'data/helpdesk.priority.csv',
		'views/helpdesk_ticket_task_info.xml',
		'views/helpdesk_po_ticket_inherit.xml',
		'views/helpdesk_crm_tickets_inherit.xml'
		],
}
