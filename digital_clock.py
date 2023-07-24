import tkinter as tk
from tkinter import colorchooser, messagebox
from time import strftime, localtime
import pygame


class DigitalClockApp(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.alarm_time = -1
        self.alarm_set_time = -1
        self.master = master
        self.master.resizable(False, False)
        self.main_bg_color = self.rgb((100, 100, 100))
        self.second_bg_color = self.rgb((170, 170, 170))
        self.time_label = tk.Label(self.master, width="7", borderwidth=2, relief="solid", bg=self.second_bg_color,
                                   fg="black", font=("LG Weather_Z", 70, "bold"))
        self.today_date_label = tk.Label(self.master, text="Today's date: {0}".format(strftime("%d/%m/%Y", localtime())),
                                         width="330", height="1", bg="white", fg="black", font=("Comic Sans MS", 20))
        self.title_label = tk.Label(self.master, text="Current Time", width="330", height="2", bg=self.main_bg_color,
                                    fg="black", font=("Comic Sans MS", 25, "bold"))
        self.change_theme_button = tk.Button(self.master, text="Change Theme", width="13", height="2",
                                             bg=self.main_bg_color, fg="black", font=("Comic Sans MS", 25, "bold"),
                                             command=self.change_theme_color)
        self.pack()
        self.create_widgets()
        master.geometry("400x450")
        master.config(bg=self.main_bg_color)
        master.title("Digital Clock")

    def create_widgets(self):
        self.title_label.pack(anchor='center')
        self.time_label.pack(anchor='center', pady=10)
        self.update_time()
        self.today_date_label.pack(anchor='center', pady=10)
        self.change_theme_button.pack(anchor='center', pady=10)

    def update_time(self):
        pygame.mixer.music.stop()
        if self.alarm_time != -1:
            time_list = [self.alarm_time, self.alarm_set_time]
            total_secs = 0
            for tm in time_list:
                time_parts = [int(s) for s in tm.split(':')]
                total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
            total_secs, sec = divmod(total_secs, 60)
            hr, mins = divmod(total_secs, 60)
            if ("%d:%02d:%02d" % (hr, mins, sec) == strftime('%H:%M:%S')):
                self.time_label.config(text="ALARM")
                pygame.mixer.music.load("alarm.ogg")
                pygame.mixer.music.play()
                messagebox.showwarning(title="Alarm!", message="Your alarm!")
                self.alarm_time = -1
        current_time = strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)

    def rgb(self, rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'

    def change_theme_color(self):
        color_code = colorchooser.askcolor(title="Choose theme color")[0]
        self.main_bg_color = self.rgb(tuple(map(int, color_code)))

        if color_code[0] >= 185 or color_code[1] >= 185 or color_code[2] >= 185:
            self.second_bg_color = self.rgb(tuple(x + (255 - int(max(color_code))) for x in (map(int, color_code))))
        else:
            self.second_bg_color = self.rgb(tuple(x + 70 for x in (map(int, color_code))))

        self.master.config(bg=self.main_bg_color)
        self.title_label.config(bg=self.main_bg_color)
        self.today_date_label.config(bg="white")
        self.change_theme_button.config(bg=self.second_bg_color)
        self.time_label.config(bg=self.second_bg_color)


if __name__ == '__main__':
    pygame.mixer.init()
    root = tk.Tk()
    app = DigitalClockApp(master=root)
    app.mainloop()
