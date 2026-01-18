import tkinter as tk
from tkinter import ttk, messagebox

class ModernPlayfairApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Playfair Cipher System")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e2e")  # Dark Background

        # Style Configuration
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#313244", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#89b4fa")], foreground=[("selected", "#1e1e2e")])

        # Creating Tabs (Pages)
        self.notebook = ttk.Notebook(root)
        self.page1 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.page2 = tk.Frame(self.notebook, bg="#1e1e2e")
        
        self.notebook.add(self.page1, text="  Encryption & Decryption  ")
        self.notebook.add(self.page2, text="  Matrix Viewer  ")
        self.notebook.pack(expand=True, fill="both")

        self.setup_page1()
        self.setup_page2()

    def setup_page1(self):
        # Page 1 UI - Title
        tk.Label(self.page1, text="PLAYFAIR CIPHER", font=("Helvetica", 20, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=20)

        # Key Input
        tk.Label(self.page1, text="Secret Key:", bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 10)).pack()
        self.key_entry = tk.Entry(self.page1, font=("Arial", 12), bg="#313244", fg="white", insertbackground="white", borderwidth=0, justify='center')
        self.key_entry.pack(pady=5, ipady=5, ipadx=10)

        # Message Input
        tk.Label(self.page1, text="Your Message:", bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 10)).pack(pady=(10,0))
        self.msg_entry = tk.Text(self.page1, height=4, width=40, font=("Arial", 11), bg="#313244", fg="white", insertbackground="white", borderwidth=0)
        self.msg_entry.pack(pady=5, padx=20)

        # Buttons
        btn_frame = tk.Frame(self.page1, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        self.enc_btn = tk.Button(btn_frame, text="ENCRYPT", command=self.encrypt_action, bg="#a6e3a1", fg="#1e1e2e", font=("Arial", 10, "bold"), width=12, relief="flat")
        self.enc_btn.pack(side="left", padx=10)

        self.dec_btn = tk.Button(btn_frame, text="DECRYPT", command=self.decrypt_action, bg="#f38ba8", fg="#1e1e2e", font=("Arial", 10, "bold"), width=12, relief="flat")
        self.dec_btn.pack(side="left", padx=10)

        # Result Output
        tk.Label(self.page1, text="Result Output:", bg="#1e1e2e", fg="#fab387", font=("Arial", 10, "bold")).pack()
        self.result_box = tk.Text(self.page1, height=4, width=40, font=("Arial", 11, "bold"), bg="#45475a", fg="#f9e2af", state='disabled', borderwidth=0)
        self.result_box.pack(pady=5, padx=20)

    def setup_page2(self):
        # Page 2 UI - 5x5 Matrix Visualizer
        tk.Label(self.page2, text="5x5 KEY MATRIX", font=("Helvetica", 18, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(pady=20)
        
        self.matrix_container = tk.Frame(self.page2, bg="#1e1e2e")
        self.matrix_container.pack(pady=10)
        
        tk.Label(self.page2, text="Note: 'J' is replaced by 'I'", font=("Arial", 9, "italic"), bg="#1e1e2e", fg="#9399b2").pack()

    def get_matrix(self, key):
        key = key.upper().replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        chars = []
        for char in key + alphabet:
            if char not in chars and char.isalpha():
                chars.append(char)
        return [chars[i:i+5] for i in range(0, 25, 5)]

    def update_matrix_display(self, matrix):
        # Clear previous matrix
        for widget in self.matrix_container.winfo_children():
            widget.destroy()
        
        for r in range(5):
            for c in range(5):
                lbl = tk.Label(self.matrix_container, text=matrix[r][c], width=4, height=2, 
                               font=("Courier", 16, "bold"), bg="#313244", fg="#89b4fa", 
                               relief="raised", borderwidth=2)
                lbl.grid(row=r, column=c, padx=3, pady=3)

    def find_pos(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char: return r, c
        return 0, 0

    def process(self, text, key, mode):
        matrix = self.get_matrix(key)
        self.update_matrix_display(matrix) # Update Page 2 matrix
        
        text = text.upper().replace('J', 'I').replace(" ", "")
        if len(text) % 2 != 0: text += 'Z'
        
        res = ""
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            if a == b: b = 'X'
            
            r1, c1 = self.find_pos(matrix, a)
            r2, c2 = self.find_pos(matrix, b)

            if r1 == r2:
                res += matrix[r1][(c1 + mode) % 5] + matrix[r2][(c2 + mode) % 5]
            elif c1 == c2:
                res += matrix[(r1 + mode) % 5][c1] + matrix[(r2 + mode) % 5][c2]
            else:
                res += matrix[r1][c2] + matrix[r2][c1]
        return res

    def encrypt_action(self):
        msg = self.msg_entry.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        if not key or not msg: return messagebox.showerror("Error", "Enter Key & Message!")
        
        result = self.process(msg, key, 1)
        self.display_result(result)

    def decrypt_action(self):
        msg = self.msg_entry.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        if not key or not msg: return messagebox.showerror("Error", "Enter Key & Message!")
        
        result = self.process(msg, key, -1)
        self.display_result(result)

    def display_result(self, text):
        self.result_box.config(state='normal')
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, text)
        self.result_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPlayfairApp(root)
    root.mainloop()
