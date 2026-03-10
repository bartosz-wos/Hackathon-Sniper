import json
import datetime
import ollama

class Brain:
    def __init__(self, model='llama3'):
        self.model = model

    def analyze(self, text, url, template):
        today = datetime.date.today().strftime('%Y-%m-%d')
        prompt = template.format(today=today, url=url, text=text)

        try:
            resp = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ], format='json')
            
            raw_output = resp['message']['content']
            return json.loads(raw_output)
        
        except Exception as e:
            return {'error': str(e), 'is_hackathon': False}

    @staticmethod
    def norm_to_bool(val):
        if isinstance(val, bool): return val
        return str(val).lower().strip() in ['true', 'tak', 'yes', '1', 't']
