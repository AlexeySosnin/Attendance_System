import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Attendance Management System")
dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
window.geometry('900x600')
window.configure(background='#01122c')


message = tk.Label(window, text="Attendance Management System", width=30, height=2, bg="#01122c",  fg="white", font=("Courier", 25, "italic bold")) 
message.place(x=10, y=10)

lbl = tk.Label(window, text="New Registration", fg="white", bg="#01122c", font=('fantasy', 18, 'bold underline') ) 
lbl.place(x=60, y=120)
lbl = tk.Label(window, text="Taking Attendance", fg="white", bg="#01122c", font=('fantasy', 18, 'bold underline') ) 
lbl.place(x=480, y=120)

lbl = tk.Label(window, text="Enter your ID:", fg="white", bg="#01122c", font=('times', 15, '') ) 
lbl.place(x=60, y=190)

txt = tk.Entry(window, width=33, bg="white", fg="black", font=('times', 16, ' '))
txt.place(x=60, y=230)

lbl2 = tk.Label(window, text="Enter your name:", fg="white", bg="#01122c", font=('times', 15, '') ) 
lbl2.place(x=60, y=270)

txt2 = tk.Entry(window,width=33, bg="white", fg="black", font=('times', 16, ' ')  )
txt2.place(x=60, y=310)

lbl3 = tk.Label(window, text="Enter your intake code:", fg="white", bg="#01122c", font=('times', 15, '') ) 
lbl3.place(x=60, y=350)

txt3 = tk.Entry(window,width=33, bg="white", fg="black", font=('times', 16, ' ')  )
txt3.place(x=60, y=390)

message = tk.Label(window, text="" ,bg="#b3d1ff", fg="black", width=30, height=3, activebackground = "yellow", font=('times', 15, ' bold ')) 
message.place(x=60, y=500)

message2 = tk.Label(window, text="", fg="red", bg="#b3d1ff", activeforeground = "green", width=33, height=3, font=('times', 15, ' bold ')) 
message2.place(x=480, y=500)

image = Image.open("face1.jpg")
photo = ImageTk.PhotoImage(image)
img_label = tk.Label(image=photo)
img_label.image = photo
img_label.place(x=510, y=190)  
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    intakeCode=(txt3.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "default_settings.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("Train_Images\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('Face recognition based Attendance system',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for [ ID : " + Id +" Name : "+ name + "\n Intake Code : " + intakeCode + " ]"
        row = [Id , name, intakeCode]
        with open('Student_Details\Student_Details.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name."
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id."
            message.configure(text= res)
        if(intakeCode == ""):
            res = "Enter your intake code!"
            message.configure(text= res)
        if(name == ""):
            res = "Enter your name!"
            message.configure(text= res)
        if(Id == ""):
            res = "Enter your ID!"
            message.configure(text= res)
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "default_settings.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("Train_Images")
    recognizer.train(faces, np.array(Id))
    recognizer.save("Train_Result\Train_result.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("Train_Result\Train_result.yml")
    harcascadePath = "default_settings.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("Student_Details\Student_Details.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','IntakeCode','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                name=df.loc[df['Id'] == Id]['Name'].values
                intakeCode=df.loc[df['Id'] == Id]['IntakeCode'].values
                tt=str(Id)+"-"+name+intakeCode
                attendance.loc[len(attendance)] = [Id,name,intakeCode,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("Unknown_Images"))+1
                cv2.imwrite("Unknown_Images\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('tracking',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)

     
takeImg = tk.Button(window, text="Take Images", command=TakeImages, bg="#1a75ff", width=10, height=1, activebackground="#0066ff", font=('times', 15, ' bold '))
takeImg.place(x=90, y=430)
trainImg = tk.Button(window, text="Train Images", command=TrainImages, bg="#1a75ff", width=10, height=1, activebackground="#0066ff", font=('times', 15, ' bold '))
trainImg.place(x=260, y=430)
trackImg = tk.Button(window, text="Track Images", command=TrackImages, bg="#1a75ff", width=10  ,height=1, activebackground="#0066ff", font=('times', 15, ' bold '))
trackImg.place(x=600, y=430)
quitWindow = tk.Button(window, text="Quit", command=window.destroy, bg="red", width=5, activebackground = "red", font=('times', 15, ' bold '))
quitWindow.place(x=820, y=10)

window.resizable(False, False)
window.mainloop()
