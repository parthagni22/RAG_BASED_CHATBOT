import json 

def load_keys():
    f = open("Data/keys.txt")
    k = "".join(f.readlines())
    keys = json.loads(k)
    f.close()
    return keys

v =load_keys()
print(v)