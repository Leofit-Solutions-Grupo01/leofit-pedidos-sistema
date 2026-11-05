import json

with open('C:/Users/Loayza/.gemini/antigravity/brain/9bdf6cf8-640a-4f22-9f23-f7cb29eb0e1d/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx == 605:
            obj = json.loads(line)
            content = obj.get('content', '')
            print(content)
            break
