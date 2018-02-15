with open('lll', 'r+', encoding='utf8') as f:
    fo = [i for i in f]
    fo .append('ff')
    fo = ''.join(fo)
    f.write(fo)
print(fo)
