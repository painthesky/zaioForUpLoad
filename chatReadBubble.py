import tkinter as tk
from tkinter import ttk
import mysql.connector

class ScrollableCanvasWithButton:
    def __init__(self, root):
        self.root = root
        self.root.title("聊天历史")
        root.iconbitmap('./生活递归_透明.ico')
        root.geometry("430x700")

        # 创建Canvas组件
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.canvas.place(relx=0.033, rely=0.022, relheight=0.899, relwidth=0.94)

        # 创建滚动条
        self.scrollbar = ttk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.set(1.0, 1.0)

        # 配置Canvas和滚动条的关联
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 创建Frame来容纳聊天气泡
        self.chat_frame = ttk.Frame(self.canvas)

        # 将Frame添加到Canvas上
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor=tk.NW)

        # 初始数据加载
        self.refresh_chat()

        self.frame2 = tk.Frame(root)
        self.frame2.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.4)
        # 在Frame底部添加一个按钮
        self.button = tk.Button(self.frame2, text="刷新")
        self.button.configure(command=self.refresh_chat)
        self.button.pack(side="bottom", fill="both")
        self.button.place(relx=0.0, rely=0.0, height=30, width=70)
        self.button2 = tk.Button(self.frame2, text="清空数据")
        self.button2.configure(command=self.delete_table)
        self.button2.pack(side="bottom", fill="both")
        self.button2.place(relx=0.5, rely=0.0, height=30, width=70)


        # 初始数据加载
        self.refresh_chat()

        self.canvas.bind("<Configure>", self.on_configure)

    def close_program(self):
	    self.root.destroy()

    def delete_table(self):
        # Get RDS connection
        self.cnx_GDAX = mysql.connector.connect(
            host="localhost",
            user="root",
            password="235623",
            database="testdb"
        )
        self.cursor = self.cnx_GDAX.cursor()

        self.cursor.execute("DROP TABLE chat_table")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender VARCHAR(20),
            message VARCHAR(6000)
        )
    """)
        self.cnx_GDAX.close()


    def on_configure(self, event):
        # 更新Canvas的scrollregion以适应新的窗口大小
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def refresh_chat(self):

        chat_data = self.do_SQL_Stuff()
        # print(chat_data)
        chat_data={'user': [item[1] for item in chat_data], 'message': [item[2] for item in chat_data]}
        # 清空聊天Frame中的内容
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        # print(chat_data['user'][4])
        # print(type(chat_data['user'][4]))
        # 显示聊天气泡
        mylen = len(chat_data['user'])

        for i in range(0, mylen):
            message = chat_data['message'][i]
            if chat_data['user'][i] == "用户":
                self.display_chat_bubble_bot(message)
            elif chat_data['user'][i] == "在哦的想法":
                self.display_chat_bubble_botthought(message)
            else:
                self.display_chat_bubble_user(message)

        # 关闭数据库连接
        # self.root.after(500, self.refresh_chat)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def do_SQL_Stuff(self):
        # Get RDS connection
        self.cnx_GDAX = mysql.connector.connect(
            host="localhost",
            user="root",
            password="235623",
            database="testdb"
        )
        self.cursor = self.cnx_GDAX.cursor()

        self.cursor.execute("SELECT * FROM chat_table")
        self.messages = self.cursor.fetchall()

        # Close RDS connection
        self.cnx_GDAX.close()
        return self.messages

    def display_chat_bubble_bot(self, message):
        # 创建Label模拟聊天气泡
        color = 'lightgreen'
        anchor = 'se'

        bubble = tk.Label(self.chat_frame, text=message, bg=color, wraplength=500, justify="left")
        bubble.pack(anchor=anchor, pady=10, padx=10)


    def display_chat_bubble_user(self, message):
        # 创建Label模拟聊天气泡

        color = 'lightblue'
        anchor = 'sw'

        bubble = tk.Label(self.chat_frame, text=message, bg=color, wraplength=500, justify="left")
        bubble.pack(anchor=anchor, pady=10, padx=10)

    def display_chat_bubble_botthought(self, message):
        # 创建Label模拟聊天气泡
        color = 'pink'
        anchor = 'sw'

        bubble = tk.Label(self.chat_frame, text=message, bg=color, wraplength=500, justify="left")
        bubble.pack(anchor=anchor, pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrollableCanvasWithButton(root)
    root.mainloop()
