import requests

class DCNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, analysis, url):
        if not self.webhook_url:
            print('Discord webhook url not found')
            return

        is_future_event = analysis.get('is_future_event')
        color = 0x00FF00 if is_future_event else 0xFF0000

        message = {
                'username': 'Hackathon Sniper',
                'embeds': [{
                    'title': f"found. {analysis.get('name', 'Unknown name')}",
                    'url': url,
                    'color': color,
                    'fields': [
                        {'name': 'location', 'value': str(analysis.get('location')), 'inline': True},
                        {'name': 'paid', 'value': str(analysis.get('is_paid')), 'inline': True},
                        {'name': 'commute refund', 'value': str(analysis.get('travel_reimbursement')), 'inline': True},
                        {'name': 'reasoning.', 'value': f"*{analysis.get('reasoning')}*", 'inline': False}
                    ],
                    'footer': {'text': 'Crazy ahh Sniper'}
                }]
        }

        try:
            requests.post(self.webhook_url, json=message)
        except Exception as e:
            print(f'message not sent, cause of {e}')
