import tkinter as tk
from multiprocessing import Process, Queue


class UserInterface:
    messages = None
    window = None
    process = None
    bus = None

    def __init__(self, bus):
        self.bus = bus

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
            self.bus.outcoming_messages.put(input_get)
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
        self.process_incoming()
        self.window.mainloop()

    # def insert_message(self, msg):
    #     self.messages.insert(tk.INSERT, 'Other: %s\n' % msg)
    #     self.messages.see('end')
    #
    # def close(self):
    #     self.process.terminate()

    def process_incoming(self):
        while self.bus.incoming_messages.qsize():
            msg = self.bus.incoming_messages.get()
            print(msg)
            self.messages.insert(tk.INSERT, 'Other: %s\n' % msg)
            self.messages.see('end')
        self.window.after(200, self.process_incoming)

# if __name__ == '__main__':
#     app = UserInterface()
#     app.show()
    # app.close()
