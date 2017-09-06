import json
data = [ { 'a':'A', 'b':{'z':'2', 'y':'4'}, 'c':3.0 } ]
outp = json.dumps(data, separators=(',',':'), sort_keys=True, indent=4)
print(outp)

