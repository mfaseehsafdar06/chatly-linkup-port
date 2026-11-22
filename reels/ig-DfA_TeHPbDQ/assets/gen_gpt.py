# Pull the 13 GPT prompts verbatim out of ASSETS.md -> assets/gpt/prompts.json
import re,json
t=open('ASSETS.md').read()
sec=t[t.index('## 3. gpt-image-2 assets'):t.index('## 4.')]
out={}
for m in re.finditer(r'\*\*(GPT-\d\d)[^*]*\*\*(.*?)(?=\n\*\*GPT-|\n---|\Z)',sec,re.S):
    p=re.search(r'\*\*Prompt:\*\*\s*\n\s*>\s*(.+)',m.group(2))
    out[m.group(1)]=p.group(1).strip()
print(len(out),list(out))
json.dump(out,open('assets/gpt/prompts.json','w'),indent=1)
