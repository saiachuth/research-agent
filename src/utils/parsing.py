import json
import re

def parse_json_output(text: str):
    """
    Parses JSON from text, handling <think> blocks and markdown code fences.
    """
    # Remove <think> blocks
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Strip markdown code blocks
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        text = match.group(1)
            
    # Attempt to parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # cleanup whitespace and try again
        text = text.strip()
        try:
            return json.loads(text)
        except:
            # Last ditch: try to find start/end braces
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end+1])
                except:
                    pass
            raise ValueError(f"Could not parse JSON from: {text}")

def clean_text_output(text: str) -> str:
    """
    Removes <think> blocks from text output.
    """
    # Remove <think> blocks
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()
