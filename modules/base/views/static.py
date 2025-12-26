import os

def serve_crm_ui(environ, start_response, module):
    """Serve the CRM UI HTML file"""
    try:
        html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'crm_ui.html')
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            start_response('200 OK', [
                ('Content-Type', 'text/html; charset=utf-8'),
                ('Content-Length', str(len(content.encode('utf-8'))))
            ])
            return [content.encode('utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'CRM UI file not found']
    
    except Exception as e:
        if module:
            module.log(f"Error serving CRM UI: {e}", "error")
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f'Error: {str(e)}'.encode('utf-8')]
