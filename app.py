import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from key_manager import generate_or_load_keys
from encryption import encrypt_message, decrypt_message
from steganography import embed_message, extract_message

# Load keys
private_key, public_key = generate_or_load_keys()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("700x500")
        self.root.config(bg="#2c3e50")

        # Title Label
        title_label = tk.Label(
            root,
            text="Steganography Tool",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=10)

        # Input Text Label and Textbox
        input_label = tk.Label(
            root,
            text="Enter your message:",
            font=("Helvetica", 12),
            fg="white",
            bg="#2c3e50"
        )
        input_label.pack(pady=(20, 5))

        self.input_text = tk.Text(root, height=6, width=60, font=("Helvetica", 10), wrap="word", bd=2, relief="groove")
        self.input_text.pack(pady=5)

        # Buttons Frame
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10), padding=10)

        encrypt_button = ttk.Button(button_frame, text="Encrypt and Embed", command=self.encrypt_and_embed)
        encrypt_button.grid(row=0, column=0, padx=10)

        decrypt_button = ttk.Button(button_frame, text="Extract and Decrypt", command=self.extract_and_decrypt)
        decrypt_button.grid(row=0, column=1, padx=10)

        # Result Text Label and Textbox
        result_label = tk.Label(
            root,
            text="Decrypted Message:",
            font=("Helvetica", 12),
            fg="white",
            bg="#2c3e50"
        )
        result_label.pack(pady=(20, 5))

        self.result_text = tk.Text(root, height=6, width=60, font=("Helvetica", 10), wrap="word", bd=2, relief="groove", state="disabled")
        self.result_text.pack(pady=5)

    def encrypt_and_embed(self):
        try:
            message = self.input_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showerror("Error", "Please enter a message to encrypt.")
                return

            image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if not image_path:
                return

            output_path = filedialog.asksaveasfilename(title="Save Image", defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if not output_path:
                return

            encrypted_message = encrypt_message(message, public_key)
            embed_message(image_path, encrypted_message.hex(), output_path)
            messagebox.showinfo("Success", f"Message embedded and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed message: {e}")

    def extract_and_decrypt(self):
        try:
            image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if not image_path:
                return

            encrypted_message_hex = extract_message(image_path)
            encrypted_message = bytes.fromhex(encrypted_message_hex)
            decrypted_message = decrypt_message(encrypted_message, private_key)

            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", decrypted_message)
            self.result_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract or decrypt message: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
