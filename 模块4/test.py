import pickle
f = open('database','rb')
r = pickle.load(f)
print(r[-1].asset)
f.close()