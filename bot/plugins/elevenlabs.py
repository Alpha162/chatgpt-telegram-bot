import datetime
import requests
import os
from typing import Dict
from .plugin import Plugin

# Load ElevenLabs API key from environment variable
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

class ElevenLabsTextToSpeech(Plugin):
    """
    A plugin to convert text to speech using ElevenLabs API
    """

    def get_source_name(self) -> str:
        return "ElevenLabs"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "elevenlabs_text_to_speech",
            "description": "Convert text to speech using ElevenLabs API",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to convert to speech"},
                    "voice_id": {"type": "string", "description": "The ElevenLabs voice ID to use"},
                    # Add other ElevenLabs specific parameters here if needed
                },
                "required": ["text", "voice_id"],
            },
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        # Here, you'll make a request to the ElevenLabs API
        # Use the requests library to send a POST request to ElevenLabs with the required data
        # Don't forget to include your ElevenLabs API key in the request headers

        response = requests.post(
            'https://api.elevenlabs.io/v1/text-to-speech/<voice-id>',
            json={
                "text": kwargs['text'],
                "model_id": "<model-id>",
                "voice_settings": {
                    # Include necessary voice settings here
                }
            },
            headers={"xi-api-key": "<your-elevenlabs-api-key>"}
        )

        output = f'elevenlabs_{datetime.datetime.now().timestamp()}.mp3'
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return {
            'direct_result': {
                'kind': 'file',
                'format': 'path',
                'value': output
            }
        }
