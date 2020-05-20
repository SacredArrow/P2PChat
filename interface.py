import tkinter as tk
from multiprocessing import Process, Queue


class UserInterface:
    messages = None
    window = None
    process = None
    msg_q = None

    def __init__(self):
        self.msg_q = Queue()

        self.window = tk.Tk()
        self.window.title("P2PChad")

        # window.geometry('500x1000')
        self.messages = tk.Text(self.window)
        scroller = tk.Scrollbar(self.window, command=self.messages.yview)
        self.messages['yscrollcommand'] = scroller.set
        scroller.pack(side='right', fill='y')
        self.messages.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        input_user = tk.StringVar()
        input_field = tk.Entry(self.window, text=input_user)
        input_field.pack(side=tk.BOTTOM, fill=tk.X)

        def Enter_pressed(event):
            input_get = input_field.get()
            self.msg_q.put(input_get)
            self.messages.insert(tk.INSERT, 'You: %s\n' % input_get)
            # label = Label(window, text=input_get)
            input_user.set('')
            # label.pack()
            self.messages.see('end')
            return "break"

        frame = tk.Frame(self.window)  # , width=300, height=300)
        input_field.bind("<Return>", Enter_pressed)
        frame.pack()

    def show(self):
        self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id())) # Place in center
        self.window.mainloop()

    def insert_message(self, msg):
        self.messages.insert(tk.INSERT, 'Other: %s\n' % msg)
        self.messages.see('end')

    def close(self):
        self.process.terminate()

# if __name__ == '__main__':
#     app = UserInterface()
#     app.show()
    # app.close()
