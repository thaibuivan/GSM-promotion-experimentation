import json
import re

with open(r'C:\Users\minhh\.gemini\antigravity-ide\brain\f66f17cc-a21a-4e2b-a2ab-0da3e51078de\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if 'USER_EXPLICIT' in line:
            if re.search(r'PM', line, re.IGNORECASE) or re.search(r'recommend', line, re.IGNORECASE):
                try:
                    data = json.loads(line)
                    print("="*50)
                    print(data.get('content'))
                except:
                    pass
