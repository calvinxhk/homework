import pickle
import array
import sys
import getopt
import re
import time
import functools


class Node:
    def __init__(self, symbol=None, right=None, left=None, weight=None):
        self.symbol = symbol
        self.right = right
        self.left = left
        self.weight = weight


def timer(wrapper):
    @functools.wraps(wrapper)
    def fun(*args, **kwargs):
        t1 = time.time()
        result = wrapper(*args, **kwargs)
        print(time.time() - t1)
        return result
    return fun


@timer
def get_content(txt):
    '得到一单词伪symbol的样本'
    rule = re.compile('[a-zA-Z]+')
    word = rule.findall(txt)
    word = set(word)
    rule = re.compile('[^a-zA-Z]')
    non_word = rule.findall(txt)
    non_word = set(non_word)
    content = word | non_word
    return content


@timer
def get_instances(content,txt):
    '获得每个字母实例化对象'
    instances = [Node(symbol=i, weight=txt.count(i)) for i in content ]
    return instances

def get_word_weight(content,txt):
    begin = 0
    end = 1
    size = len(txt)
    weight_dict ={key:0 for key in content }
    while end <= size:
        if txt[begin:end].isalpha():
            end +=1
        else:
            if not txt[begin:end -1]:
                weight_dict[txt[begin]] +=1
                begin += 1
                end  += 1
            else:
                weight_dict[txt[begin:end-1]] +=1
                begin = end -1
    return weight_dict

@timer
def get_word_instances(content,txt):
    weight_dict = get_word_weight(content,txt)
    instances = [Node(symbol=i, weight=weight_dict[i]) for i in content]
    return instances

@timer
def build_tree(instances):
    '创建霍夫曼树'

    while len(instances) > 1:
        instances.sort(key=lambda x: x.weight)
        huff_tree = Node(left=instances[0],right = instances[1],weight = instances[0].weight + instances[1].weight)
        del instances[0]
        del instances[0]
        instances.append(huff_tree)
    return instances[0]


@timer
def get_code_dict(huff_tree):
    '得到实例：编码的字典'
    code_dict = {}
    code = ''
    code_dict[huff_tree] = code
    while len(code_dict) < len(content):
        new_code_dict = {}
        for key in code_dict:
            if key.left:
                new_key = key.left
                new_code_dict[new_key] = code_dict[key] + '0'
            if key.right:
                new_key = key.right
                new_code_dict[new_key] = code_dict[key] + '1'
            else:
                new_code_dict[key] = code_dict[key]
        code_dict = new_code_dict
    return code_dict


@timer
def get_symbol(code_dict):
    '得到symbol：编码的字典'
    new_code_dict = {key.symbol:code_dict[key] for key in code_dict }
    return new_code_dict


@timer
def get_newtxt(txt,new_code_dict):
    '得到编码后有0与1组成的文本'
    new_txt = ''
    for i in txt:
        new_txt += '%s' % new_code_dict[i]
    return new_txt


@timer
def get_word_newtxt(txt, new_code_dict):
    index_begin = 0
    index_end = 1
    size = len(txt)
    file = ''
    while index_end <= size:
        if txt[index_begin:index_end].isalpha():
            index_end += 1
        else:
            if txt[index_begin:index_end - 1]:
                code = new_code_dict[txt[index_begin:index_end - 1]]
                file += code
                index_begin = index_end - 1
            else:
                code = new_code_dict[txt[index_begin]]
                file += code
                index_begin = index_end
                index_end = index_begin + 1
    return file


@timer
def final_code(new_txt):
    '没八位组成一个字节，写入文件'
    with open('infile.bin', 'wb') as f:
        index = 0
        spare = len(new_txt) % 8
        codearray = array.array('B')
        if not spare:
            spare = 8
        index_end = len(new_txt) -spare
        while index < index_end:
            content = new_txt[index:index + 8]
            content = int(content, 2)
            codearray.append(content)
            index += 8
        txt_end = new_txt[-spare:]
        zero = re.match('0+',txt_end)
        if zero:
            num_zero = len(re.match('0+',txt_end).group())
        else:
            num_zero = 0
        codearray.append(num_zero)
        codearray.append(int(new_txt[-spare:],2))
        codearray.tofile(f)



opt, args = getopt.getopt(sys.argv[1:], 's:')
with open('infile.txt', 'r', encoding='utf8') as f:
    txt = f.read()
for op, value in opt:
    if op == '-s' and value == 'char':
        content = set(txt)
        instances = get_instances(content,txt)
        huff_tree = build_tree(instances)
        code_dict = get_code_dict(huff_tree)
        new_code_dict = get_symbol(code_dict)
        with open('infile_symbol_model.pkl', 'wb') as f:
            pickle.dump(new_code_dict, f)
        new_txt = get_newtxt(txt,new_code_dict)
        final_code(new_txt)
    elif op == '-s' and value == 'word':
        content = get_content(txt)
        instances = get_word_instances(content,txt)
        huff_tree = build_tree(instances)
        code_dict = get_code_dict(huff_tree)
        new_code_dict = get_symbol(code_dict)
        with open('infile_symbol_model.pkl', 'wb') as f:
            pickle.dump(new_code_dict, f)
        new_txt = get_word_newtxt(txt,new_code_dict)
        final_code(new_txt)
