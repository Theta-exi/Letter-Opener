import random
from pyperclip import copy as pc
from time import perf_counter_ns

boomQ = False
boom = 0

# 开字符
def ocha(*args):
    for char in args:
        if char in opened_Character:
            raise Exception("已开:" + char)
    opened_Character.extend(args)

# 关字符
def ccha(*args):
    global opened_Character
    for char in args:
        if char not in opened_Character:
            raise Exception("未开:" + char)
    opened_Character = [char for char in opened_Character if char not in args]

# 打开答案
def oans(*args):
    for number in args:
        number = int(number)
        if number < 1 or n_Sum < number:
            raise Exception("出界:" + str(number))
        if opened_Answer[number-1]:
            raise Exception("已开:" + str(number))
    global boom
    for number in args:
        number = int(number)
        opened_Answer[number-1] = True
        boom += 1

# 关闭答案
def cans(*args):
    for number in args:
        number = int(number)
        if number < 1 or n_Sum < number:
            raise Exception("出界:" + str(number))
        if not opened_Answer[number-1]:
            raise Exception("未开:" + str(number))
    global boom
    for number in args:
        number = int(number)
        opened_Answer[number-1] = False
        boom -= 1

# 逐个打开
def osin(*args):
    for p in args:
        x, y = eval(p)
        if x < 1 or n_Sum < x:
            raise Exception("索引出界:" + str(x))
        if y < 1 or len(string_Matrix[x - 1]) < y:
            raise Exception(f"长度出界:({str(x)},{str(y)})")
    for p in args:
        x, y = eval(p)
        string_Matrix[x - 1][y - 1][0] = True

# 逐个关闭
def csin(*args):
    for p in args:
        x, y = eval(p)
        if x < 1 or n_Sum < x:
            raise Exception("索引出界:" + str(x))
        if y < 1 or len(string_Matrix[x - 1]) < y:
            raise Exception(f"长度出界:({str(x)},{str(y)})")
    for p in args:
        x, y = eval(p)
        string_Matrix[x - 1][y - 1][0] = False

# 设置炸弹模式
def setboom(n):
    global boomQ
    if n == '1':
        boomQ = True
    else:
        boomQ = False

# 设置炸弹数
def setb(n):
    global boom
    boom = int(n)

# 是否打开（内置函数不可使用）
def is_Open(x, y):
    return opened_Answer[x - 1] or string_Matrix[x - 1][y - 1][1] in opened_Character or string_Matrix[x - 1][y - 1][0]

# 技能：空袭——打开指定未开字符，周围未开的字符的十字型内概率打开，概率默认1/3
def airp(x, y):
    x, y = int(x), int(y)
    if x < 1 or n_Sum < x:
        raise Exception("索引出界:" + str(x))
    if y < 1 or len(string_Matrix[x - 1]) < y:
        raise Exception(f"长度出界:({str(x)},{str(y)})")
    if is_Open(x, y):
        raise Exception("该格已开，应使用mine")
    global boom
    string_Matrix[x - 1][y - 1][0] = True
    for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if i < 1 or n_Sum < i or j < 1 or len(string_Matrix[i - 1]) < j:
            continue
        if random.random() < 1 / 3:
            string_Matrix[i - 1][j - 1][0] = True
    boom -= 1

# 技能：扫雷——在已开的字符周围3×3的格子中，未开的字符概率打开，至少打开一个，概率默认1/3
def mine(x, y):
    x, y = int(x), int(y)
    if x < 1 or n_Sum < x:
        raise Exception("索引出界:" + str(x))
    if y < 1 or len(string_Matrix[x - 1]) < y:
        raise Exception(f"长度出界:({str(x)},{str(y)})")
    if not is_Open(x, y):
        raise Exception("该格未开，应使用airp")
    global boom
    close = [p for p in [(x - 1, y), (x + 1, y), 
                         (x, y - 1), (x, y + 1), 
                         (x - 1, y - 1), (x + 1, y + 1), 
                         (x + 1, y - 1), (x - 1, y + 1)] if p[0] > 0 and p[0] <= n_Sum and p[1] > 0 and p[1] <= len(string_Matrix[p[0] - 1]) and not is_Open(*p)]
    opening = random.randint(1, len(close))
    t = 1
    for i, j in close:
        if t == opening or random.random() < 1 / 3:
            string_Matrix[i - 1][j - 1][0] = True
        t += 1
    boom -= 1

# 智能技能施放
def b(x, y):
    if is_Open(int(x), int(y)):
        mine(x, y)
    else:
        airp(x, y)

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
                alternate_Strings = [line.strip() for line in f.readlines() 
                                     if line[0] != "#" and line.strip() != ""]
        except FileNotFoundError:
            print("文件不存在,请重试")
            continue
        n = int(input("抽取数量(1~"+ str(len(alternate_Strings)) + "):"))
        n_Sum += n
        add_Strings = random.sample(alternate_Strings, n)
        selected_Strings.extend(add_Strings)
        # print(add_Strings)
        i += 1
    random.shuffle(selected_Strings)
    string_Matrix = [[[False, char] for char in string] for string in selected_Strings]
    show_Answers = input("是否显示答案(y/n):")
    if show_Answers == "y":
        answer_String = ""
        for i, string in enumerate(selected_Strings):
            answer_String += f"{i+1}.{string}\n"
        print(answer_String)
        pc(answer_String)
    endQ = False
    opened_Character = []
    opened_Answer = [False] * n_Sum
    while not endQ:
        command = input("开字母或键入'/'输入指令(特殊符号请自行转义):")
        if command and command[0] == "/":
            sequence = command[1:].split(" ")
            for i, stri in enumerate(sequence[1:]):
                stri = stri.replace("\\", "\\\\")
                stri = stri.replace("\"", "\\\"")
                sequence[i + 1] = "\"" + stri + "\""
                sequences = ",".join(sequence[1:])
            cmd = f"{sequence[0]}({sequences})"
            try:
                eval(cmd)
            except Exception as e:
                print(e)
        else:
            if command[:2] == "--":
                opened_Character = [char for char in opened_Character if char not in command[2:]]
            else:
                for char in command:
                    if char not in opened_Character:
                        opened_Character.append(char)
        final_String = "已开" + "".join(opened_Character) + "\n"
        endQ = True
        for i, string in enumerate(string_Matrix):
            if opened_Answer[i]:
                final_String += f"{i+1}.{selected_Strings[i]}"
            else:
                final_String += f"{i+1}."
                oansQ = True
                for boolean, char in string:
                    if boolean or char in opened_Character:
                        final_String += char
                    else:
                        endQ = False
                        oansQ = False
                        final_String += "*"
                if oansQ:
                    opened_Answer[i] = True
                    boom += 1
            final_String += "\n"
        final_String += "未猜出数量：" + str(n_Sum - sum(opened_Answer))
        if boomQ:
            final_String += "\n炸弹可用次数：" + str(boom)
        print(final_String)
        pc(final_String)
        if endQ and input("是否继续操作(y/n):") == "y":
            endQ = False
    input("请按任意键退出")