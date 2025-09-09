import requests
import json
import os
from datetime import datetime, timezone
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_tip(category: str) -> dict:
    """
    Generate a tech tip using Gemini API
    Returns a dictionary with the structure needed for TipCreate
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': os.getenv('GEMINI_KEY')
    }
    
    prompt = f"""Generate a practical tech tip about {category} with these specifications:
    1) Title: 4 to 7 words max. It should be catchy but not verbose, catchy and descriptive
    2) Content: 1 to 2 sentences only. Must be clear, focused, and useful to developers immediately.
    3) Code example: 1 to 4 lines of clean, short, relevant code. 
    4) Hashtags: Exactly 3, with no commas or curly braces, just a string with 3 hashtags, only # on each, use widely-recognized tags in twitter.
    
    Do not exceed the specified length for each section.
    Format the response strictly as JSON using these keys: title, content, code, hashtags.
    Make it practical and immediately useful for developers."""
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Try to parse JSON from the response
        try:
            # First, try to extract JSON from markdown code blocks
            if "```json" in generated_text:
                # Extract content between ```json and ```
                start = generated_text.find("```json") + 7
                end = generated_text.find("```", start)
                if end != -1:
                    json_text = generated_text[start:end].strip()
                    tip_data = json.loads(json_text)
                else:
                    raise json.JSONDecodeError("No closing markdown block found", "", 0)
            else:
                # Try to parse the entire response as JSON
                tip_data = json.loads(generated_text)
        except json.JSONDecodeError:
            # If not valid JSON, create a simple structure
            tip_data = {
                "title": f"Tech Tip: {category}",
                "content": generated_text[:200] + "..." if len(generated_text) > 200 else generated_text,
                "code_example": None,
                "hashtags": f"#{category.replace(' ', '')} #TechTip"
            }
        
        # Return in the format expected by TipCreate
        return {
            "category": category,
            "title": tip_data["title"],
            "content": tip_data["content"],
            "code_example": tip_data.get("code"),
            "hashtags": tip_data["hashtags"],
            "is_ai_generated": True,
            "created_at": datetime.now(timezone.utc)
        }
        
    except Exception as e:
        # Return a fallback tip if API fails
        return {
            "category": category,
            "title": f"Tech Tip: {category}",
            "content": f"Here's a useful tip about {category}. Always keep learning!",
            "code_example": None,
            "hashtags": "#DailyTechTip #Coding",
            "is_ai_generated": True,
            "created_at": datetime.now(timezone.utc)
        }

