import pandas as pd
import requests
from tkinter import *

bg="#000000"
fg="#FFFFFF"

data = requests.get("https://m.cricbuzz.com/cricket-pointstable/3130/indian-premier-league-2020sa")
# print(data.text)

df=pd.read_html(data.text)[0]
root = Tk()

root.geometry('800x500')

root.config (bg = bg)

Label(root, text="IPL Points Table",font=('TIMES NEW ROMAN',15,'bold','underline'),fg = fg, bg=bg,pady=30).pack()

data = df.to_string(header = True, index = False).replace(""," ") 
Label(root, text = data,justify = RIGHT,font=('Arial',10), fg = fg, bg=bg,pady=20, borderwidth=2, relief="groove", highlightcolor="white").pack()
root.mainloop()