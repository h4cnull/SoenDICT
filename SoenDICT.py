#coding=utf-8
#author: https://github.com/h4cnull

import optparse
import json
import sys
import os
import csv
from probability import comm_probability

ALL_PASSWORD = []

def get_templates(tmpl_content):
    tmpls = []
    lines = [ line.strip() for line in tmpl_content.split("\n") ]
    keys = set([])
    for line in lines:
        tmpl = line.split()
        keys = keys.union(set(tmpl))
        tmpls.append(tmpl)
    return tmpls,keys

def check_elements(elements_keys,tmpl_keys):
    for k in tmpl_keys:
        if k not in elements_keys:
            return False
    return True

def genPwd(elements,index=0,headstr="",prob=0):
    if index >= len(elements):
        return
    words = elements[index]
    for w in words:
        w = str(w)
        try:
            p = comm_probability[w]
        except:
            p = 1                 #没有在概率表里的元素概率为1
        p += prob
        if index < len(elements)-1:
            genPwd(elements,index+1,headstr+w,p)
        else:
            ALL_PASSWORD.append([headstr+w,p,len(elements)])

def get_file_name(file_path):
    file = os.path.basename(file_path)
    tmp = file.split(".")
    if len(tmp) == 1:
        return tmp[0]
    else:
        return ".".join(tmp[:-1])

if __name__ == '__main__':
    parser = optparse.OptionParser('')
    parser.add_option('-e', '--element', dest = 'element_file', type = 'string', help = '元素文件')
    parser.add_option('-t', '--template', dest = 'template_file', type = 'string', help = '模板文件')
    parser.add_option('-l', '--length', dest = 'max_length', type = 'int', default=12, help = '密码最大长度')
    parser.add_option('-o', '--out', dest = 'out_file', type = 'string', help = '输出文件名前缀(默认"元素文件_模板文件"名)')
    (options,args) = parser.parse_args()
    if options.element_file == None or options.template_file == None:
        parser.print_help()
        sys.exit(-1)

    if options.out_file == None:
        out_file_name = "{}_{}.csv".format(get_file_name(options.element_file),get_file_name(options.template_file))
    else:
        out_file_name = options.out_file + ".csv"
    
    try:
        out_file = open(out_file_name,'w',newline='')
    except Exception as e:
        print("[!] 打开输出文件错误 {}".format(out_file_name))
        sys.exit(-1)

    try:
        element_file = open(options.element_file,'r',encoding='utf-8')
    except FileNotFoundError:
        print("[!] 没有找到元素文件 {}".format(options.element_file))
        sys.exit(-1)

    try:
        tmpl_file = open(options.template_file,'r',encoding='utf-8')
        tmpl_content = tmpl_file.read()
    except FileNotFoundError:
        print("[!] 没有找到模板文件 {}".format(options.template_file))
        sys.exit(-1)
    
    elements = json.load(element_file)
    elements_keys = elements.keys()
    tmpls,tmpl_keys = get_templates(tmpl_content)
    if len(tmpl_keys) > 0 and len(elements_keys) > 0:
        current_path = os.getcwd()
        element_path_dir = os.path.dirname(os.path.join(current_path,element_file.name))

        for tmpl in tmpls:   #一个模板
            #print(tmpl)
            order_list = []
            elements_key_file = None
            tmpl_valid = True
            for key in tmpl:
                if key not in elements.keys():
                    tmpl_valid = False
                    break
                if type(elements[key]).__name__ == "list":
                    if len(elements[key]) == 0:
                        tmpl_valid = False
                        break
                    order_list.append(elements[key])
                else:
                    try:
                        f_p = os.path.join(element_path_dir,str(elements[key]))
                        f = open(f_p,'r',encoding='utf-8')
                        tmp = [ line.strip() for line in f.readlines() ]
                        if len(tmp) == 0:
                            tmpl_valid = False
                            break
                        order_list.append(tmp)
                    except FileNotFoundError:
                        elements_key_file = f_p
            if not tmpl_valid:
                continue
            if elements_key_file:
                print("[!] 没有找到元素文件{}中{}指定的文件 {}, 所在模板 {}".format(element_file.name,key,elements_key_file,tmpl_file.name))
                continue
            genPwd(order_list)
        writer = csv.writer(out_file)
        writer.writerow(['password','probability'])
        print("[-] 结果保存至：{}".format(out_file_name))
        for p in ALL_PASSWORD:
            if len(p[0]) <= options.max_length:
                pwd = p[0]
                prob = p[1]/p[2]
                #print("{} , {}".format(pwd,prob))
                writer.writerow([pwd,prob])
    else:
        print("[!] 模板{}或元素{}文件为空".format(tmpl_file.name,element_file.name))
    