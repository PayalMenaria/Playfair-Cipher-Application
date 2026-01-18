import tkinter as tk
from tkinter import messagebox

class PlayfairCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Playfair Cipher - Encryption/Decryption")
        self.root.geometry("400x450")

        # Labels and Inputs
        tk.Label(root, text="Enter Key:", font=("Arial", 10, "bold")).pack(pady=5)
        self.key_entry = tk.Entry(root, width=30)
        self.key_entry.pack(pady=5)

        tk.Label(root, text="Enter Message:", font=("Arial", 10, "bold")).pack(pady=5)
        self.msg_entry = tk.Text(root, height=4, width=35)
        self.msg_entry.pack(pady=5)

        # Buttons
        self.enc_btn = tk.Button(root, text="Encrypt", command=self.encrypt_msg, bg="lightblue", width=15)
        self.enc_btn.pack(pady=10)

        self.dec_btn = tk.Button(root, text="Decrypt", command=self.decrypt_msg, bg="lightgreen", width=15)
        self.dec_btn.pack(pady=5)

        tk.Label(root, text="Result:", font=("Arial", 10, "bold")).pack(pady=5)
        self.result_entry = tk.Text(root, height=4, width=35, state='disabled')
        self.result_entry.pack(pady=5)

    def prepare_key(self, key):
        key = key.upper().replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = []
        for char in key + alphabet:
            if char not in matrix and char.isalpha():
                matrix.append(char)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_pos(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def process_text(self, text, matrix, mode):
        text = text.upper().replace('J', 'I').replace(" ", "")
        # Prepare digraphs
        res = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if (i+1) < len(text) else 'Z'
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
            
            r1, c1 = self.find_pos(matrix, a)
            r2, c2 = self.find_pos(matrix, b)

            if r1 == r2: # Same Row
                res += matrix[r1][(c1 + mode) % 5]
                res += matrix[r2][(c2 + mode) % 5]
            elif c1 == c2: # Same Column
                res += matrix[(r1 + mode) % 5][c1]
                res += matrix[(r2 + mode) % 5][c2]
            else: # Rectangle rule
                res += matrix[r1][c2]
                res += matrix[r2][c1]
        return res

    def encrypt_msg(self):
        key = self.key_entry.get()
        msg = self.msg_entry.get("1.0", tk.END).strip()
        if not key or not msg:
            messagebox.showwarning("Error", "Please enter both Key and Message")
            return
        matrix = self.prepare_key(key)
        encrypted = self.process_text(msg, matrix, 1)
        self.show_result(encrypted)

    def decrypt_msg(self):
        key = self.key_entry.get()
        msg = self.msg_entry.get("1.0", tk.END).strip()
        if not key or not msg:
            messagebox.showwarning("Error", "Please enter both Key and Message")
            return
        matrix = self.prepare_key(key)
        decrypted = self.process_text(msg, matrix, -1)
        self.show_result(decrypted)

    def show_result(self, text):
        self.result_entry.config(state='normal')
        self.result_entry.delete("1.0", tk.END)
        self.result_entry.insert(tk.END, text)
        self.result_entry.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayfairCipherApp(root)
    root.mainloop()
