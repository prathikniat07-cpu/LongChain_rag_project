import json
with open('Handson_lab1.ipynb', 'r', encoding='utf-8') as f:
    data = f.read()
data = data.replace('"localhost"', '"127.0.0.1"')
with open('Handson_lab1.ipynb', 'w', encoding='utf-8') as f:
    f.write(data)
