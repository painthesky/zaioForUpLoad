import tkinter as tk
from openai import OpenAI
import mysql.connector
import constants
import os

# 连接到你的 MySQL 数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="235623",
    database="testdb"
)

os.environ["OPENAI_API_KEY"] = constants.APIKEY

with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender VARCHAR(20),
            message VARCHAR(6000)
        )
    """)
conn.commit()

client = OpenAI()


def submit():
    input_text = entry.get()

    with open('./能力列表.txt', 'r', encoding='utf-8') as file:
        # 读取整个文件内容
        content = file.read()
        # Get RDS connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT message "
                       "FROM chat_table "
                       "WHERE sender = '用户'"
                       "ORDER BY id DESC "
                       "LIMIT 10")
        messages = cursor.fetchall()

    # input_text_alter = content + "\""+input_text+"\"\n" + "进行非常简要的回答"
    input_text_alter = "\""+input_text+"\"\n"+ content
    for message in messages:
        input_text_alter = input_text_alter+"\n"+str(message[0])
    # 从输入框获取文本

    msg_to_LLM = [
            {"role": "system", "content": "你是一个语义判断机器，你只用单个英文字母或者单个数字提交你的判断,比如\"a\",\"b\"，当你不知道的时候回复\"n\""},
            {"role": "user", "content": input_text_alter}
        ]
    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=msg_to_LLM
    )
    thought01 = completion.choices[0].message.content
    with conn.cursor() as cursor:

        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("用户", input_text))
        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("在哦的想法", thought01))

    conn.commit()

    if thought01 == "h":
        output = "小卖部在一楼的北面，咖啡厅在二楼的北面，你现在在哪里"
    elif thought01 == "b":
        output = "可以窗口缴费，也可以机器缴费。推荐机器缴费，你觉得可以么？"
    elif thought01 == "c":
        output = "可以窗口缴费，也可以机器缴费。推荐机器缴费，你觉得可以么？"
    elif thought01 == "d":
        output = "取药窗口在一楼大厅西侧，取药窗口有很多，你知道自己应该在几号窗口取药么？"
    elif thought01 == "e":
        output = "就医需要先挂号，您已经有挂号条了对么？\n您需要我调用数据,猜猜您的病情该如何治疗么？"
    elif thought01 == "f":
        output = "请您立刻像周围的人请求救助，我已经把你的资料上传系统，请您稍作等待"
    elif thought01 == "g":
        output = "一楼二楼三楼都有厕所，您现在在哪？"
    elif thought01 == "i":
        output = "现在医生是要您去取药还是做检查呢？"
    elif thought01 == "j":
        output = "您接下来应该看医生吧？\n您知道自己去哪个科室么？"
    elif thought01 == "k":
        output = "您缴费的项目是什么？\n挂号，还是检查，还是药费？"
    elif thought01 == "l":
        output = "您知道药应该怎么吃吧？\n您知道离开医院回家的路吧？"
    elif thought01 == "m":
        output = "结果出来了么？\n如果出来了，那就等于您的病历更新了。你需要找医生再问诊一遍吧？"
    elif thought01 == "n":
        output = "如果您在等待，我们可以完善一下最新的病历，您想么？"
        take_user_data(input_text)
    elif thought01 == "a":
        output = ask_gpt_directly(input_text)
    else:
        output = ask_gpt_directly(input_text)

    # 在标签中显示提交的内容
    label.config(text="你刚刚提交的内容是: " + input_text_alter)
    label2.config(text="在哦：" + output)

    # 打开文件（如果文件不存在，会创建一个新文件）


    with conn.cursor() as cursor:

        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("在哦", output))

    conn.commit()

def submit_case02():
    input_text = entry.get()

    with open('./是非问题.txt', 'r', encoding='utf-8') as file:
        # 读取整个文件内容
        content = file.read()

    # input_text_alter = content + "\""+input_text+"\"\n" + "进行非常简要的回答"
    input_text_alter2 = "\""+input_text+"\"\n"+ content
    # 从输入框获取文本

    msg_to_LLM2 = [
            {"role": "system", "content": "你是一个语义判断机器，你只用单个英文字母或者单个数字提交你的判断,比如\"a\",\"b\"，当你不知道的时候回复\"n\""},
            {"role": "user", "content": input_text_alter2}
        ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=msg_to_LLM2
    )
    thought01 = completion.choices[0].message.content
    with conn.cursor() as cursor:

        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("用户", input_text))
        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("在哦的想法", thought01))

    conn.commit()

    if thought01 == "b":
        output = "那我们现在开始填病历。"
    elif thought01 == "c":
        output = "好的知道了"
        submit_button.config(command=submit)
    elif thought01 == "a":
        output = ask_gpt_directly(input_text)
        submit_button.config(command=submit)
    else:
        output = ask_gpt_directly(input_text)
        submit_button.config(command=submit)

    # 在标签中显示提交的内容
    label.config(text="你刚刚提交的内容是: " + input_text_alter2)
    label2.config(text="在哦：" + output)

    # 打开文件（如果文件不存在，会创建一个新文件）


    with conn.cursor() as cursor:

        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("在哦", output))

    conn.commit()

def take_user_data(input_text):
    submit_button.config(command=submit_case02)
    return None

def ask_gpt_directly(input_text):

    with conn.cursor() as cursor:
        cursor.execute("SELECT message "
                       "FROM chat_table "
                       "WHERE sender = ('用户', '在哦')"
                       "ORDER BY id DESC "
                       "LIMIT 30")
        messages = cursor.fetchall()

    # input_text_alter = content + "\""+input_text+"\"\n" + "进行非常简要的回答"
    input_text_alter = "结合以上聊天记录回答：\""+input_text+"\"\n"
    for message in messages:
        input_text_alter = message[0]+"\n"+input_text_alter

    with conn.cursor() as cursor:

        cursor.execute("INSERT INTO chat_table (sender, message) VALUES (%s, %s)", ("在哦的想法", input_text_alter))

    conn.commit()
    # 从输入框获取文本
    msg_to_LLM = [
            {"role": "system", "content": "你的名字叫在哦。你是一个可以犯错的答题者，大多数情况下你喜欢简要的回答问题。你不说不知道，不知道的时候也要猜一个答案。"},
            {"role": "user", "content": input_text_alter}
        ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=msg_to_LLM
    )
    output_text = completion.choices[0].message.content

    return output_text

# 创建Tkinter窗口
root = tk.Tk()
root.title("询问openai")
root.iconbitmap('D:\gui\生活递归_透明.ico')
root.geometry("600x700")

# 创建提交按钮
submit_button = tk.Button(root, text="提交", command=submit, width=60)
submit_button.pack(pady=10,side='bottom')

# 创建输入框
entry = tk.Entry(root, width=60)
entry.pack(pady=10,side='bottom')

# 创建标签，用于显示提交的内容
label2 = tk.Label(root, text="", wraplength=400)
label2.pack(pady=10,side='bottom')

# 创建标签，用于显示提交的内容
label = tk.Label(root, text="", wraplength=400)
label.pack(pady=10,side='bottom')



# 运行主事件循环
root.mainloop()