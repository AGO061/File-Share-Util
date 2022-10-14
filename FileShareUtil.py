import requests
import json
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import qrcode
import sys
if len(sys.argv)==1:
    messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nNo file was specified.")
    exit("File Error")
upfile=sys.argv[1]
url = 'https://tmpfiles.org/api/v1/upload'
try:
    myfiles = {'file': open(upfile,'rb')}
except:
    messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nFile name is invalid.")
    exit("File Name Error")
print("uploading...")
x = requests.post(url, files = myfiles)

#print the response text (the content of the requested file):
response=json.loads(x.text)
if (response["status"]!="success"):
    messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nServer returned status: \"{response['status']}\".")
    exit("Upload Error")
finalurl=response["data"]["url"]
#Creating an instance of qrcode
qr = qrcode.QRCode(
        version=1,
        box_size=5,
        border=5)
qr.add_data(finalurl)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
#img.save('qrcode001.png')
root=Tk()
root.title("File Share Util: "+upfile)
QrImage=ImageTk.PhotoImage(img)
label_image = Label(image=QrImage)
entry_text = StringVar()
UrlEntry=Entry(root,textvariable=entry_text,state="readonly",fg="black",bg="white")
entry_text.set(finalurl)

label_image.pack()
UrlEntry.pack()
root.mainloop()

