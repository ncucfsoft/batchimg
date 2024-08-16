import tkinter as tk
import numpy as np
import configparser
import windnd
import os
import base64
from qq import img
from PIL import Image
from tkinter import messagebox
from tkinter import filedialog
from windnd import hook_dropfiles
def resizeimg(filepath):
    global global_var1
    global global_var2    
    global global_varselect
    try:
        image =Image.open(filepath) 
        if(global_varselect.get()=="1"):
            scale_percent=int(global_var1.get())
            print("缩放比例："+str(scale_percent))
            # 计算缩放后的新尺寸
            width = int(image.width * scale_percent / 100)
            height = int(image.height * scale_percent / 100)
        else:
            width=int(global_var2.get())
            height=int(image.height*width/image.width)
            print("width height"+str(width)+str(height))
   
        dim = (width, height)
        resized_image = image.resize(dim)
        resized_image.save(filepath)
    except:
        messagebox.showinfo('操作失败',filepath+'不是一个有效的jpg或png文件!' )
def show():
      
   
    file_path = filedialog.askopenfilenames(title='请选择一个或多个图片文件', initialdir='', filetypes=[( "图片文件", ".jpg .png"), ('All Files', ' *')])
    file_list=[]
    if file_path:
        for file in file_path:
         print("选择的文件:"+file)
         resizeimg(file)

        
         #image = cv2.imread(file)
        # image = cv2.imdecode(newfilename, cv2.IMREAD_COLOR)
        #image =Image.open(file)
       
         
         
         #dim = (width, height)
         #resized_image = image.resize(dim)
         #resized_image.save(file)
         #resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
         #encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
 # 保存调整大小后的图像
         #cv2.imwrite(newfilename, resized_image)
         #if file.lower().find(".png") != -1:
         # cv2.imencode('.png',resized_image)[1].tofile(file)
         #else:
         # cv2.imencode('.jpg',resized_image,encode_params)[1].tofile(file) 

    messagebox.showinfo('操作完成','全部转换完毕!' )

def test(content):
    # 如果不加上==""的话，就会发现删不完。总会剩下一个数字 isdigit函数：isdigit函数方法检测字符串是否只由数字组成。
    if content.isdigit() or content == "":
        return True
    else:
        return False   
def on_focus_in1(event):
        global_varselect.set("1")

def on_focus_in2(event):
        global_varselect.set("2")

def dragged_files(files):
    for file_path in files:
        file_path = file_path.decode('gbk')      
        resizeimg(file_path)     
    messagebox.showinfo('操作完成','全部转换完毕!' ) 
    ##pyinstaller -i qq.ico -F -w test7.py 
def main(): 
    root = tk.Tk()
    
    global global_var1
    global_var1=tk.StringVar()
  

    global global_var2
    global_var2=tk.StringVar()
   
    
    global global_varselect
    global_varselect=tk.StringVar()
    config = configparser.ConfigParser()
 

    config.read('imgbatch.ini')

    global_varselect.set(config.get('Section1', 'select', fallback='1'))
    global_var1.set(config.get('Section1', '缩放百分比', fallback='50'))
    global_var2.set(config.get('Section1', '指定宽度像素大小', fallback='900'))
 
    def on_close():
     print("退出程序")
     root.quit()  # 终止事件循环  
     if not config.has_section('Section1'):
      config.add_section('Section1')
     config.set('Section1', 'select',global_varselect.get())
     config.set('Section1', '缩放百分比',global_var1.get())
     config.set('Section1', '指定宽度像素大小',global_var2.get())
     
     with open('imgbatch.ini', 'w') as configfile:
        config.write(configfile)

    root.protocol("WM_DELETE_WINDOW", on_close) 
    #tk.Label(root, text = "").grid(row=0,column=0)
    #tk.Label(root, text = "").grid(row=1,column=1)
    tk.Label(root, text = "                   ").grid(row=0,column=0)
    

    #tk.Label(root, text="按百分比缩放：").grid(row=2, column=3,sticky="w")
    #tk.Label(root, text="按指定像素大小：").grid(row=3, column=3,sticky="w")
    rb_male = tk.Radiobutton(root, text='按百分比缩放', variable=global_varselect, value='1')
    rb_male.grid(row=0, column=1, padx=20, pady=20,sticky="w")
    rb_female = tk.Radiobutton(root, text='按指定宽度像素大小', variable=global_varselect, value='2')
    rb_female.grid(row=1, column=1, padx=20, pady=20,sticky="w")

    test_cmd = root.register(test)
    e1 = tk.Entry(root,textvariable=global_var1,validate = "key",validatecommand = (test_cmd, '%P'))
    e1.grid(row=0, column=2)

    e2 = tk.Entry(root,textvariable=global_var2,validate = "key",validatecommand = (test_cmd, '%P'))
    e2.grid(row=1, column=2)
    
   
    
    tk.Button(root, text="浏览", width=10, command=show).grid(row=2, column=1, sticky="w", padx=10, pady=5)
    tk.Button(root, text="退出", width=10, command=on_close).grid(row=2, column=2, sticky="e", padx=10, pady=5)
    root.title("选择批量修改文件尺寸的多个图片文件")
    root.resizable(False,False)
    
   
    e1.bind("<FocusIn>", on_focus_in1)
    e2.bind("<FocusIn>", on_focus_in2)
    def setIcon():
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))  # 写入到临时文件中
        tmp.close()
        root.iconbitmap("tmp.ico")  # 设置图标
        os.remove("tmp.ico")  # 删除临死图标
    #root.wm_attributes('-type', 'dialog')
    # 设置窗口大小
    width=500
    height=200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
    setIcon() # 应用函数
    hook_dropfiles(root, func=dragged_files)
    root.mainloop()
if __name__ == "__main__":
    main()