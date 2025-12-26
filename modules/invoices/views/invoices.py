def list_invoices(environ, start_response, module):
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    invoices = invoice_service.list_invoices(session)
    return module.response(start_response, {'invoices': [i.__dict__ for i in invoices]})

def create_invoice(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    invoice = invoice_service.create_invoice(session, body)
    module.emit_event('invoice_created', {'invoice_id': invoice.id})
    return module.response(start_response, {'invoice': invoice.__dict__}, '201 Created')

def get_invoice(environ, start_response, module):
    invoice_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    invoice = invoice_service.get_invoice(session, invoice_id)
    if invoice:
        return module.response(start_response, {'invoice': invoice.__dict__})
    return module.response(start_response, {'error': 'Invoice not found'}, '404 Not Found')

def update_invoice(environ, start_response, module):
    invoice_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    invoice = invoice_service.update_invoice(session, invoice_id, body)
    if invoice:
        module.emit_event('invoice_updated', {'invoice_id': invoice.id})
        return module.response(start_response, {'invoice': invoice.__dict__})
    return module.response(start_response, {'error': 'Invoice not found'}, '404 Not Found')

def delete_invoice(environ, start_response, module):
    invoice_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    if invoice_service.delete_invoice(session, invoice_id):
        module.emit_event('invoice_deleted', {'invoice_id': invoice_id})
        return module.response(start_response, {'message': 'Invoice deleted'})
    return module.response(start_response, {'error': 'Invoice not found'}, '404 Not Found')

def add_payment(environ, start_response, module):
    invoice_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['invoice_id'] = invoice_id
    session = module.get_db_session()()
    invoice_service = module.env.get_service('invoices_invoice_service')
    payment = invoice_service.add_payment(session, body)
    module.emit_event('payment_received', {'payment_id': payment.id, 'invoice_id': invoice_id})
    return module.response(start_response, {'payment': payment.__dict__}, '201 Created')
