from modules.newsletter.models import Subscriber, Campaign
from datetime import datetime

def list_subscribers(environ, start_response, newsletter_module):
    try:
        newsletter_module.log("Listing all subscribers", "info")
        subscribers = Subscriber.all()
        return newsletter_module.response(start_response, {'subscribers': subscribers})
        
    except Exception as e:
        newsletter_module.log(f"Error listing subscribers: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def subscribe(environ, start_response, newsletter_module):
    try:
        body = newsletter_module.get_body(environ)
        if not body:
            return newsletter_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        email = body.get('email')
        company_id = body.get('company_id')
        
        if not all([email, company_id]):
            return newsletter_module.response(start_response, {'error': 'Email and company_id are required'}, '400 Bad Request')
        
        existing = Subscriber.get(email=email, company_id=company_id)
        if existing:
            if existing['is_active']:
                return newsletter_module.response(start_response, {'error': 'Email already subscribed'}, '400 Bad Request')
            else:
                subscriber = Subscriber.update_record(existing['id'], is_active=True, unsubscribed_at=None)
        else:
            subscriber_data = {
                'company_id': company_id,
                'email': email,
                'name': body.get('name'),
                'customer_id': body.get('customer_id')
            }
            subscriber = Subscriber.create(**subscriber_data)
        
        newsletter_module.log(f"New subscriber: {subscriber['email']}", "info")
        
        newsletter_module.emit_event('newsletter_subscribed', {
            'subscriber_id': subscriber['id'],
            'company_id': subscriber['company_id'],
            'email': subscriber['email']
        })
        
        return newsletter_module.response(start_response, {'success': True, 'subscriber': subscriber})
        
    except Exception as e:
        newsletter_module.log(f"Error subscribing: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def unsubscribe(environ, start_response, newsletter_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        subscriber_id = route_params.get('id')
        
        if not subscriber_id:
            return newsletter_module.response(start_response, {'error': 'Subscriber ID is required'}, '400 Bad Request')
        
        subscriber = Subscriber.update_record(subscriber_id, is_active=False, unsubscribed_at=datetime.utcnow())
        if not subscriber:
            return newsletter_module.response(start_response, {'error': 'Subscriber not found'}, '404 Not Found')
        
        newsletter_module.log(f"Subscriber unsubscribed: {subscriber['email']}", "info")
        
        newsletter_module.emit_event('newsletter_unsubscribed', {
            'subscriber_id': subscriber['id'],
            'email': subscriber['email']
        })
        
        return newsletter_module.response(start_response, {'success': True})
        
    except Exception as e:
        newsletter_module.log(f"Error unsubscribing: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def list_campaigns(environ, start_response, newsletter_module):
    try:
        newsletter_module.log("Listing all campaigns", "info")
        campaigns = Campaign.all()
        return newsletter_module.response(start_response, {'campaigns': campaigns})
        
    except Exception as e:
        newsletter_module.log(f"Error listing campaigns: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_campaign(environ, start_response, newsletter_module):
    try:
        body = newsletter_module.get_body(environ)
        if not body:
            return newsletter_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        name = body.get('name')
        subject = body.get('subject')
        content = body.get('content')
        company_id = body.get('company_id')
        
        if not all([name, subject, content, company_id]):
            return newsletter_module.response(start_response, {'error': 'Name, subject, content, and company_id are required'}, '400 Bad Request')
        
        campaign_data = {
            'company_id': company_id,
            'name': name,
            'subject': subject,
            'content': content,
            'created_by': 1
        }
        
        campaign = Campaign.create(**campaign_data)
        newsletter_module.log(f"Campaign created: {campaign['name']}", "info")
        
        newsletter_module.emit_event('campaign_created', {
            'campaign_id': campaign['id'],
            'company_id': campaign['company_id'],
            'name': campaign['name']
        })
        
        return newsletter_module.response(start_response, {'success': True, 'campaign': campaign})
        
    except Exception as e:
        newsletter_module.log(f"Error creating campaign: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_campaign(environ, start_response, newsletter_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        campaign_id = route_params.get('id')
        
        if not campaign_id:
            return newsletter_module.response(start_response, {'error': 'Campaign ID is required'}, '400 Bad Request')
        
        campaign = Campaign.get(id=campaign_id)
        if not campaign:
            return newsletter_module.response(start_response, {'error': 'Campaign not found'}, '404 Not Found')
        
        return newsletter_module.response(start_response, {'campaign': campaign})
        
    except Exception as e:
        newsletter_module.log(f"Error getting campaign: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def send_campaign(environ, start_response, newsletter_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        campaign_id = route_params.get('id')
        
        if not campaign_id:
            return newsletter_module.response(start_response, {'error': 'Campaign ID is required'}, '400 Bad Request')
        
        campaign = Campaign.get(id=campaign_id)
        if not campaign:
            return newsletter_module.response(start_response, {'error': 'Campaign not found'}, '404 Not Found')
        
        if campaign['status'] == 'sent':
            return newsletter_module.response(start_response, {'error': 'Campaign already sent'}, '400 Bad Request')
        
        active_subscribers = Subscriber.filter(is_active=True)
        
        campaign = Campaign.update_record(campaign_id, status='sent', sent_at=datetime.utcnow())
        
        newsletter_module.log(f"Campaign sent: {campaign['name']} to {len(active_subscribers)} subscribers", "info")
        
        newsletter_module.emit_event('campaign_sent', {
            'campaign_id': campaign['id'],
            'name': campaign['name'],
            'subscriber_count': len(active_subscribers)
        })
        
        return newsletter_module.response(start_response, {
            'success': True, 
            'campaign': campaign,
            'sent_to': len(active_subscribers)
        })
        
    except Exception as e:
        newsletter_module.log(f"Error sending campaign: {e}", "error")
        return newsletter_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
