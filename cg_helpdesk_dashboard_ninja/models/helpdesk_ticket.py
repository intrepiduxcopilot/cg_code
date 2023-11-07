from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class CustomHelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    b2c_b2b = fields.Selection([
        ('b2c', 'B2C (Hogar)'),
        ('b2b', 'B2B (Negocio)')
    ], string='Tipo de Cliente')

    # Etapa 1 estatus

    status_selection = fields.Selection([
        ('aa','Nuevo'),
        ('a', 'Por Cotizar'),
        ('b', 'Cotizados'),
        ('c', 'Por Aprob'),
        ('d', 'Desestimado'),
    ], string='Estatus ticket', default='aa')
    # Pendiente requerir asignar otro status si no se esta en la etapa Nuevo

    # lost = fields.Boolean(string='Perdido', default=False, compute='_compute_lost', store=True)

    # def _compute_lost(self):
    #     for ticket in self:
    #         ticket.lost = ticket.status_selection == 'd'

    # preguntas etapas 1, 2 y 3


    #control de calidad etapa  y cobro 2 
    calidad_tiempo_respuesta = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Tiempo de Resp del Servicio',default="1")
    calidad_funcionamiento = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Funcionamiento del servicio',default="1")
    calidad_actitud_aptitud = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Actitud/aptitud del técnico',default="1")
    calidad_expectativas = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Expectativas del servicio',default="1")
    calidad_satisfaccion_precios = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Satisfacción en precios ofrecidos',default="1")
    fecha_autorizacion_cobros = fields.Date(string='Fecha para Autorización de Cobros', default=date.today() + timedelta(days=1))
    avg_etapa2 = fields.Float(string='Promedio Etapa 2', compute='_compute_avg_etapa2')

    @api.depends('calidad_tiempo_respuesta', 'calidad_funcionamiento', 'calidad_actitud_aptitud', 'calidad_expectativas', 'calidad_satisfaccion_precios')
    def _compute_avg_etapa2(self):
        for record in self:
            # Calculate the average
            total_scores = (
                int(record.calidad_tiempo_respuesta) +
                int(record.calidad_funcionamiento) +
                int(record.calidad_actitud_aptitud) +
                int(record.calidad_expectativas) +
                int(record.calidad_satisfaccion_precios)
            )
            
            # calculando promedio de los campos
            if total_scores != 0:
                avg_etapa2 = (total_scores / 5)*10
                # se multiplica x 10 para llevarlo a base 100
            else:
                avg_etapa2 = 0

            record.avg_etapa2 = avg_etapa2

        
            

    metodo_pago = fields.Selection([
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
        ('cheque', 'Cheque'),
        ('otros', 'Otros'),
    ], string='Metodo de pago')
    

    @api.constrains('fecha_autorizacion_cobros')
    def _check_future_date(self):
        for record in self:
            if record.fecha_autorizacion_cobros and record.fecha_autorizacion_cobros <= date.today():
                raise ValidationError('La fecha de autorización de cobros debe ser una fecha futura.')


    
    etapa1 = fields.Char(string='Etapa 1', compute='_compute_etapa1') 
    #verificar este campo en la vista para mostrar grupos de preguntas segun sea el caso

    @api.depends('stage_id')
    def _compute_etapa1(self):
        for record in self:
            if record.stage_id:
                record.etapa1 = record.stage_id.sequence
                # si esta en la etapa 1, cambia el estatus a Por cotizar
                record.status_selection = 'a' if record.etapa1 == '2' else record.status_selection
                print(record.status_selection)
            else:
                record.etapa1 = False  # 2 == etapa 1; 3== etapa 2;

    # En la etapa 3 se debe manejar por contabilidad  ya que todos los campos afectan facturas. y los detalles 
    #  que se desean obtener es parte de la contabilidad de costos/analitico

    #etapa 4 
    calidad_servicio = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Dentro de un rango del 1 al 10,ud entiende que se manejó la empresa con respecto a la calidad del servicio?', default='1')
    presupuesto_precio = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Que le pareció el Presupuesto y/o Precios?',default='1')
    gestion_cobro = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='Que le pareció la Gestión de Cobros',default='1')
    avg_etapa3 = fields.Float(string='Promedio Etapa 3', compute='_compute_avg_etapa3')
    
    @api.depends('calidad_servicio', 'presupuesto_precio', 'gestion_cobro')
    def _compute_avg_etapa3(self):
        for record in self:
            # Calculate the average
            total_scores = (
                int(record.calidad_servicio) +
                int(record.presupuesto_precio) +
                int(record.gestion_cobro)
            )

            # calculando promedio de los campos
            if total_scores != 0:
                avg_etapa3 = (total_scores / 3)*10
                # se multiplica x 10 para llevarlo a base 100
            else:
                avg_etapa3 = 0

            record.avg_etapa3 = avg_etapa3

    # calidad_servicio = fields.Selection([(str(i), str(i)) for i in range(1, 11)], string='En general que tan satisfecho quedó con el servicio, en un rango del 1 al 10?')
    servicio_sugerencia = fields.Text(string="Alguna Recomendación para Mejorar los servicios?")
    referencias = fields.Many2many('res.partner', string='Referencias ')
    