import random
from pyperclip import copy as pc
from time import perf_counter_ns

def refresh_String():
    global opened_Character, opened_Number
    opened_String = input("要打开的字符串(n重星号后为n位序号):")
    serial = -1
    serial_Number = ""
    cancel = False
    for i in opened_String:
        if i == "-" and serial == 1:
            cancel = True
            serial = -1
            continue
        if i == "*":
            if serial == -1:
                serial = 1
            else:
                serial += 1
        else:
            if serial > 0:
                if i.isdigit():
                    serial_Number += i
                else:
                    print("序号错误:星号过多,使用较短的序号:" + serial_Number)
                    opened_Character.append(i)
                    if 0 < int(serial_Number) <= n:
                        if cancel:
                            try:
                                opened_Number.remove(int(serial_Number))
                            except ValueError:
                                print("警告:序号未打开")
                            cancel = False
                        else:
                            opened_Number.append(int(serial_Number))
                    serial_Number = ""
                    serial = -1
                    continue
                serial -= 1
            if serial == 0:
                if 0 < int(serial_Number) <= n:
                    if cancel:
                        try:
                            opened_Number.remove(int(serial_Number))
                        except ValueError:
                            print("警告:序号"+serial_Number+"未打开")
                        cancel = False
                    else:
                        opened_Number.append(int(serial_Number))
                serial_Number = ""
                serial = -1
                continue
            if serial < 0:
                if cancel:
                    try:
                        opened_Character.remove(i)
                    except ValueError:
                        print("警告:字符"+i+"未打开")
                    cancel = False
                else:
                    opened_Character.append(i)
    opened_Character = list(set(opened_Character))
    opened_Number = list(set(opened_Number))
    opened_Character.sort()

def refresh_Hidden():
    global hidden_List, opened_Number
    hidden_List = selected_Strings.copy()
    for i in range(len(hidden_List)):
        if i+1 not in opened_Number:
            chars_To_Replace = closed_Character - set(opened_Character)
            for char in chars_To_Replace:
                hidden_List[i] = hidden_List[i].replace(char,"*")
            if hidden_List[i] == selected_Strings[i]:
                opened_Number.append(i+1)
                opened_Number=list(set(opened_Number))

def output_Format():
    str0 = "已开" + "".join(opened_Character)
    for i, str1 in enumerate(hidden_List):
        str0 += f"\n{i+1}.{str1}"
    return str0

if __name__ == "__main__":
    selected_Strings = []
    random.seed(perf_counter_ns())
    print("注意：每次输出都已将结果粘贴进剪贴板。\n文件名不要有特殊符号")
    file_Num = int(input("文件数量:"))
    n_Sum = 0
    i = 1
    while i <= file_Num:
        rul = input(str(i) + ".拖入txt文件直接回车").replace("\"","")
        rul = rul.replace("'","")
        rul = rul.replace("& ","")
        try:
            with open(rul, "r", encoding="utf-8") as f:
                alternate_Strings = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("文件不存在,请重试")
            continue
        n = int(input("抽取数量(1~"+ str(len(alternate_Strings)) + "):"))
        n_Sum += n
        add_Strings = random.sample(alternate_Strings, n)
        selected_Strings.extend(add_Strings)
        print(add_Strings)
        i += 1
    pinYin = input("注音或罗马音?(y/n):")
    if pinYin == "y":
        print("将逐个补充,格式:空格+(拼音或罗马音)")
        for i in range(n_Sum):
            pinYin_String = input(str(i) + ".")
            selected_Strings[i] = selected_Strings[i] + pinYin_String
    random.shuffle(selected_Strings)
    closed_Character = set("".join(selected_Strings))
    opened_Character = []
    show_Answers = input("是否显示答案(y/n):")
    if show_Answers == "y":
        opened_Number = range(1, n_Sum + 1)
        refresh_Hidden()
        answer_String = output_Format()
        print(answer_String)
    opened_Number = []
    while len(opened_Number) < n_Sum:
        refresh_String()
        refresh_Hidden()
        final_String = output_Format()
        print(final_String)
        pc(final_String)
    input("请按任意键继续. . .")