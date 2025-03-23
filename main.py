import tkinter as tk
from tkinter import messagebox
from random import choice


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")  # Set window size
        self.remaining_time = 60
        self.timer_started = False
        self.cpm_value = 0
        self.wpm_value = self.cpm_value / 5

        #Get 100 random words from the word list
        self.word_list = []
        self.words = []
        with open("word_list.txt") as file:
            for line in file:
                w = line.split(" ")
                if "'" not in w[0] and "." not in w[0] and len(w[0]) > 1:
                    self.word_list.append(w[0])
        self.generate_words()

        # Create and pack the main frames
        self.result_frame = tk.Frame(root, bg="gray15", padx=10, pady=10)
        self.text_frame = tk.Frame(root, bg="gray15", padx=10, pady=10)
        self.input_frame = tk.Frame(root, bg="gray15", padx=10, pady=10)
        self.result_frame.pack(fill="both", expand=True)
        self.text_frame.pack(fill="both", expand=True)
        self.input_frame.pack(fill="both", expand=True)

        #Add widgets to the result frame
        self.add_result_widgets()

        # Add widgets to the text frame
        self.add_text_widgets()

        # Add widgets to the input frame
        self.add_input_widgets()

    def add_result_widgets(self):
        # Corrected Characters per minute label
        self.cpm = tk.Label(self.result_frame, text=f"Corrected CPM : {self.cpm_value}",
                            font=("Arial", 12, "bold"),
                            bg="gray15", fg="SteelBlue3",
                            pady=5, padx=10)
        self.cpm.grid(row=0, column=0)

        # Words per minute label
        self.wpm = tk.Label(self.result_frame, text=f"WPM : {self.wpm_value}", font=("Arial", 12, "bold"),
                            bg="gray15", fg="SteelBlue3",
                            pady=5, padx=10)
        self.wpm.grid(row=0, column=1)

        #Time left label
        self.time_left = tk.Label(self.result_frame, text="Time left : 60", font=("Arial", 12, "bold"),
                                  bg="gray15", fg="SteelBlue3", pady=5, padx=10)
        self.time_left.grid(row=0, column=2)

        #Restart button
        self.restart_button = tk.Button(self.result_frame, text="Restart", command=self.restart,
                                        fg="gray15", bg="SteelBlue3", font=("Arial", 12, "bold"))
        self.restart_button.grid(row=0, column=6, sticky='e')

        self.result_frame.grid_columnconfigure(6, weight=1)

    def add_text_widgets(self):
        # Add random words + center each line
        self.text = tk.Text(self.text_frame, height=11, width=280, wrap="word", bd=0,
                            font=("Arial", 16, "bold"), fg="midnight blue", bg="grey80")
        self.text.insert("1.0", " ".join(self.words))
        self.text.config(state="disabled")
        self.text.pack(pady=10)
        self.text.tag_config("center", justify='center')
        self.text.tag_add("center", "1.0", "end")

        #Add tags for checking the user input
        self.text.tag_config("correct", foreground="forest green")
        self.text.tag_config("incorrect", foreground="firebrick3")

    def add_input_widgets(self):
        # Text Widget (Multi-line Text)
        self.atext = tk.Text(self.input_frame, height=11, width=100, bd=3, font=("Arial", 14, "bold"),
                             fg="midnight blue", bg="gray80", wrap="word")
        self.atext.pack(pady=10)
        self.atext.bind("<Key>", self.start_timer)

        # Key release event will update CPM and WPM in real time
        self.atext.bind("<KeyRelease>", self.update_cpm_wpm)

        # Disable control-v(paste)
        self.atext.bind('<Control-v>', lambda _: 'break')

    def start_timer(self, event):
        if not self.timer_started:
            self.timer_started = True
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_left.config(text=f"Time left: {self.remaining_time}")
            self.root.after(1000, self.update_timer)
        else:
            self.atext.config(state='disabled')

            #Calculate accuracy
            total_characters = self.cpm_value + self.incorrect_char_count
            if total_characters > 0:
                accuracy = (self.cpm_value / total_characters) * 100
            else:
                accuracy = 0

            # Show message box with results
            messagebox.showinfo(
                "Time's Up!",
                f"Characters per minute: {self.cpm_value}\n"
                f"Words per minute: {self.wpm_value}\n"
                f"Accuracy: {accuracy:.2f}%"
            )

    def generate_words(self):
        self.words = [choice(self.word_list) for _ in range(100)]

    def update_cpm_wpm(self, event):
        # Remove old tags
        self.text.tag_remove("correct", "1.0", "end")
        self.text.tag_remove("incorrect", "1.0", "end")

        #Counter for correct/incorrect characters
        correct_char_count = 0
        self.incorrect_char_count = 0

        # Get user input without the last newline
        user_input = self.atext.get("1.0", "end-1c")
        target_text = " ".join(self.words)

        # Compare input with the text and apply the correct/incorrect tag
        for i in range(len(user_input)):
            if i < len(target_text):
                if user_input[i] == target_text[i]:
                    correct_char_count += 1
                    self.text.tag_add("correct", f"1.{i}", f"1.{i+1}")
                else:
                    self.incorrect_char_count += 1
                    self.text.tag_add("incorrect", f"1.{i}", f"1.{i + 1}")


        #Calculate CPM
        self.cpm_value = correct_char_count
        self.cpm.config(text=f"Corrected CPM : {self.cpm_value}")

        #Divide by 5 to get the WPM
        self.wpm_value = self.cpm_value / 5
        self.wpm.config(text=f'WMP : {self.wpm_value}')

    def restart(self):
        # Reset the timer
        self.remaining_time = 60
        self.timer_started = False
        self.time_left.config(text=f"Time left: {self.remaining_time}")

        # Reset input
        self.atext.config(state='normal')
        self.atext.delete("1.0", tk.END)

        # Reset + generate new words
        self.generate_words()
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", " ".join(self.words))
        self.text.tag_add("center", "1.0", "end")
        self.text.config(state="disabled")

        # Reset labels
        self.cpm_value = 0
        self.wpm_value = self.cpm_value / 5
        self.cpm.config(text=f"Corrected CPM : {self.cpm_value}")
        self.wpm.config(text=f"WPM : {self.wpm_value}")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    app = MyApp(root)
    root.mainloop()
