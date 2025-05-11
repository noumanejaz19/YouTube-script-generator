"""
Script generation utilities using OpenAI API.
"""

import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

class ScriptGenerator:
    def __init__(self):
        """Initialize the script generator with OpenAI API client."""
        # Load API key and validate it
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Validate API key format (should start with 'sk-')
        if not api_key.startswith('sk-'):
            raise ValueError("Invalid OPENAI_API_KEY format. It should start with 'sk-'")
            
        # Create a custom httpx client
        http_client = httpx.Client(
            timeout=60.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Initialize OpenAI client with the custom http client
        self.client = OpenAI(
            api_key=api_key,
            http_client=http_client
        )
        
    def generate_script(self, title: str, transcript: str, word_count: int) -> Optional[str]:
        """
        Generate a script based on the title and transcript.
        
        Args:
            title (str): The new video title
            transcript (str): The inspirational video transcript
            word_count (int): Desired word count for the script
            
        Returns:
            Optional[str]: Generated script or None if generation fails
        """
        try:
            # Calculate number of parts needed based on word count
            # Assuming each part is around 1000 words
            num_parts = (word_count + 999) // 1000
            
            prompt = f"""Write a complete YouTube script with the following requirements:

1. Title: {title}
2. Total word count: {word_count} words
3. Number of parts: {num_parts}
4. Each part should be approximately {word_count // num_parts} words
5. Use the following transcript as inspiration for structure and style:
{transcript}

Important instructions:
- Write ONLY the script content, no meta-commentary or explanations
- Include scene descriptions, dialogue, and narration
- Maintain consistent formatting with clear scene transitions
- Do not include any meta-text like "I will provide" or "Here's the script"
- Do not include any promotional text or calls to action
- Focus on storytelling and scene development
- Ensure the total word count is exactly {word_count} words

Format the script with clear scene headings, dialogue, and narration as follows:

### [Scene Heading]
[Scene description]
[Character Name]: [Dialogue]
[Narration]

[Continue with next scene...]"""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a professional script writer. Write only the script content without any meta-commentary or promotional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating script: {str(e)}")
            return None
            
    def regenerate_segment(self, title: str, transcript: str, segment_index: int, previous_segments: list) -> Optional[str]:
        """
        Regenerate a specific segment of the script.
        
        Args:
            title (str): The video title
            transcript (str): The inspirational video transcript
            segment_index (int): Index of the segment to regenerate
            previous_segments (list): List of previous segments
            
        Returns:
            Optional[str]: Regenerated segment or None if generation fails
        """
        try:
            context = "\n\n".join(previous_segments[:segment_index])
            
            prompt = f"""I need you to regenerate part {segment_index + 1} of the story with title: {title}
            The story should be inspired by this transcript:
            {transcript}
            
            Here is the context from previous parts:
            {context}
            
            Please generate a new version of part {segment_index + 1} that maintains consistency with the previous parts
            but offers a fresh perspective or alternative approach. The segment should be 800-1000 words long."""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a professional script writer who specializes in creating engaging YouTube content. Your scripts should be well-structured, engaging, and maintain viewer interest throughout."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error regenerating segment: {str(e)}")
            return None 