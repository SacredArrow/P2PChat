from bus import Message, MessageType
import tkinter as tk


class UserInterface:
    messages = None
    window = None
    process = None
    pub = None

    def __init__(self, pub):
        self.pub = pub
        self.pub.subscribe(self, ["incoming", "server_closed"])

        self.window = tk.Tk()
        self.window.title("P2PChad")
        self.window.protocol('WM_DELETE_WINDOW', self.onClose)

        # window.geometry('500x1000')
        self.messages = tk.Text(self.window)
        scroller = tk.Scrollbar(self.window, command=self.messages.yview)
        self.messages['yscrollcommand'] = scroller.set
        scroller.pack(side='right', fill='y')
        self.messages.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        input_user = tk.StringVar()
        input_field = tk.Entry(self.window, text=input_user)
        input_field.pack(side=tk.BOTTOM, fill=tk.X)

        def enter_pressed(event):
            input_get = input_field.get()
            msg = Message(input_get, MessageType.CLIENT_MESSAGE)
            self.pub.send_message(msg, "outgoing")

            self.messages.insert(tk.INSERT, 'You: %s\n' % input_get)
            # label = Label(window, text=input_get)
            input_user.set('')
            # label.pack()
            self.messages.see('end')
            return "break"

        frame = tk.Frame(self.window)  # , width=300, height=300)
        input_field.bind("<Return>", enter_pressed)
        frame.pack()

    def onClose(self):
        close_msg = Message("client closed", MessageType.CLIENT_CLOSED)
        self.pub.send_message(close_msg, "client_closed")
        self.window.destroy()

    def show(self):
        self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_toplevel())
        self.process_incoming()
        self.window.mainloop()

    def process_incoming(self):
        for msg in self.pub.get_messages(self):
            if msg.type == MessageType.SERVER_CLOSED:
                close_msg = Message("client closed", MessageType.CLIENT_CLOSED)
                self.pub.send_message(close_msg, "client_closed")
                # TODO: implement application termination
                exit(0)

            self.messages.insert(tk.INSERT, 'Other: %s\n' % msg.text)
            self.messages.see('end')
        self.window.after(200, self.process_incoming)
