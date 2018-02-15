import pickle,functools,time


def Timer(wrapper):
    @functools.wraps(wrapper)
    def func(*args,**kwargs):
        t = time.time()
        result = wrapper(*args,**kwargs)
        print(time.time() - t)
        return result
    return func


@Timer
def get_dict():
    with open('infile_symbol_model.pkl', 'rb') as f:
        code = pickle.load(f)
        code_dict = {}
        for key in code:
            code_dict[code[key]] = key
    return code_dict


@Timer
def get_txt():
    with open('infile.bin', 'rb') as f:
        txt = f.read()
        last = txt[-1]
        txt_del_end = txt[:-1]
        new_txt = ''
        for i in txt_del_end:
            code = bin(i)[2:]
            size = len(code)
            if size < 8:
                code = '0' * (8 - size) + code
            new_txt += code
        code = bin((last))[2:]
        new_txt += code
    return new_txt


@Timer
def write_txt(txt,code_dict):
    index_begin = 0
    index_end = 1
    size = len(txt)
    with open('infile_decompressed.txt', 'w') as f:
        file = ''
        while index_end <= size:
            if txt[index_begin:index_end] in code_dict:
                file += code_dict[txt[index_begin:index_end]]
                index_begin = index_end
                index_end = index_begin + 1
            else:
                index_end += 1
        f.write(file)

code_dict = get_dict()
txt = get_txt()
write_txt(txt,code_dict)
