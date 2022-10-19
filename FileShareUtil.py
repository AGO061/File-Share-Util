import requests
import json
import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import qrcode
import sys
import ctypes
if sys.platform.startswith('win'):
    import winreg
FILENAME="FileShareUtil.exe"
REGISTRY="*\\shell\\FSU"

def exit(x):
    sys.exit(x)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if len(sys.argv)==1:
    if sys.platform.startswith('win'): #Open registry setter
        if is_admin():
            enable=messagebox.askyesno(title="Registry menu adder",message=f"Press yes if you want to add the option\n\"Upload with FSU\"\nto your explorer right-click menu")
            if enable:
                root=winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)
                winreg.CreateKey(root,REGISTRY)
                winreg.CreateKey(root,REGISTRY+"\\command")
                winreg.SetValue(root,REGISTRY,winreg.REG_SZ,"Upload with FSU")
                winreg.SetValue(root,REGISTRY+"\\command",winreg.REG_SZ,"\""+os.path.abspath(os.getcwd()+"/"+FILENAME).replace("/","\\")+"\" \"%V\"")
                fsu=winreg.OpenKeyEx(root, REGISTRY, reserved=0, access=winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(fsu,"Icon",0,winreg.REG_SZ,os.path.abspath(os.getcwd()+"/"+FILENAME).replace("/","\\"))
                winreg.CloseKey(fsu)
                winreg.CloseKey(root)
                messagebox.showinfo(title="SUCCESS!",message=f"The option has been added to the menu!")
                exit("Installed succefully")
            else:
                exit("Not adding registry key")
        else:
            messagebox.showerror(title="ERROR!",message=f"To open the registry menu adder, please run the program as admin")
            exit("File Error")
    else: #Just throw an error
        messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nNo file was specified.")
        exit("File Error")

upfile=os.path.abspath(sys.argv[1]).replace("\\","/")
print(upfile)
url = "https://tmpfiles.org/api/v1/upload"

try:
    myfiles = {'file': open(upfile,'rb')}
except:
    messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nFile name is invalid.")
    exit("File Name Error")

print("uploading...")

x = requests.post(url, files = myfiles)

#print the response text (the content of the requested file):

response=json.loads(x.text)
print(response)
try:
    if (response["message"]=="Server Error"):
        messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nServer Error.")
        quit("Server Error")
except:
    pass
try:
    if (response["status"]!="success"):
        messagebox.showerror(title="ERROR UPLOADING!",message=f"ERROR!\nServer returned status: \"{response['status']}\".")
        quit("Upload Error")
except:
    pass

finalurl=response["data"]["url"]

# Creating an instance of qrcode

qr = qrcode.QRCode(version=1,box_size=5,border=5)
qr.add_data(finalurl)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')

# Main window
root=Tk()
root.title("FSU: "+upfile.split("/")[-1:][0])
root.iconbitmap("icon.ico")
QrImage=ImageTk.PhotoImage(img)
label_image = Label(image=QrImage)
entry_text = StringVar()
UrlEntry=Entry(root,textvariable=entry_text,state="readonly",fg="black",bg="white")
entry_text.set(finalurl)
creditslbl=Label(root,text="This project was possible thanks to tmpfiles.org")

label_image.pack()
UrlEntry.pack()
creditslbl.pack(side="bottom")
root.mainloop()

