from flask import Flask, render_template, url_for, request,jsonify
import sqlite3
import os
import telepot

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
cursor.execute("create table if not exists voting(party TEXT, voter TEXT, place TEXT, candidate TEXT)")
command = """CREATE TABLE IF NOT EXISTS admin(email TEXT, password TEXT)"""
cursor.execute(command)
command = """CREATE TABLE IF NOT EXISTS user(userid TEXT, voterid TEXT, name TEXT, phone TEXT, address TEXT)"""
cursor.execute(command)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM admin WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('adduser.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
            

    return render_template('index.html')

@app.route('/userlog')
def userlog():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM user"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        import cv2
        import os
        import time
        import numpy as np
        import time
        import pandas as pd
        ##recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cam = cv2.VideoCapture(0)
        ncount = []
        count = 0
        while True:
                ret, im =cam.read()
                gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2,5)
                for(x,y,w,h) in faces:
                    count += 1
                    cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 4)
                    Id,i = recognizer.predict(gray[y:y+h,x:x+w])
                    print(Id, i)
                    Id = str(Id)
                    if i < 60:
                        query = "SELECT name FROM user WHERE userid = '"+Id+"'"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        print(result)
                        name = result[0]
                        ncount.append(name)
                        cv2.putText(im, name, (x,y-40), font, 2, (255,255,255), 3)
                    else:
                        ncount.append("unknown")
                        cv2.putText(im, "unknown", (x,y-40), font, 2, (255,255,255), 3)
                cv2.imshow('im',im)
                if cv2.waitKey(500) & count >= 10:
                    break
        cam.release()
        cv2.destroyAllWindows()
        counter = 0
        for i in ncount:
            curr_frequency = ncount.count(i)
            if(curr_frequency > counter):
                counter = curr_frequency
                num = i
        print(num)
        if num != "unknown":
            query = "SELECT * FROM user WHERE name = '"+num+"'"
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)
            
            f = open('session.txt', 'w')
            f.write(result[1])
            f.close()

            return render_template('userlog.html', result=result[0])
        else:
            return render_template('index.html', msg='Sorry, face mismathced')
    else:
        return render_template('index.html', msg='Voting list is empty')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        party = request.form['party']
        place = request.form['place']
        name = request.form['name']
        f = open('session.txt',  'r')
        voter = f.readline()
        f.close()

        con = sqlite3.connect('user_data.db')
        cr = con.cursor()
        cr.execute("select * from voting where voter = '"+voter+"'")
        result = cr.fetchall()
        if result:
            return render_template('index.html', msg='Already your oting process completed')
        else:
            print(party, voter, place, name)
            con = sqlite3.connect('user_data.db')
            cr = con.cursor()
            cr.execute("insert into voting values('"+party+"', '"+voter+"', '"+place+"', '"+name+"')")
            con.commit()
            return render_template('index.html', msg='Voting process successsfully completed')
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        voterid = request.form['voterid']
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        userid = request.form['userid']
        otp = int(request.form['otp'])
        print(userid)
        cursor.execute("select * from user where userid = '"+userid+"' or voterid = '"+voterid+"' or phone = '"+phone+"'")
        result = cursor.fetchall()

        print(result)
        if result:
            return render_template('adduser.html', msg='user id or voter id already exists')
        else:
            f = open('OTP.txt', 'r')
            otp1 = f.readline()
            otp1 = int(otp1)
            f.close()

            print(userid, voterid, name, phone, address)
            if otp == otp1:
                import cv2
                vid_cam = cv2.VideoCapture(0)
                face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                count = 0
                while(True):
                    _, image_frame = vid_cam.read()
            
                    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)
                    for (x,y,w,h) in faces:
                        cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
                        count += 1
                        cv2.imwrite("dataset/"+name+"." + str(userid) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('frame', image_frame)
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    elif count>100:
                        break
                vid_cam.release()
                cv2.destroyAllWindows()

                import cv2
                import os
                import numpy as np
                from PIL import Image
                #recognizer = cv2.face.createLBPHFaceRecognizer()
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                def getImagesAndLabels(path):
                    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
                    faceSamples=[]
                    ids = []
                    for imagePath in imagePaths:
                        PIL_img = Image.open(imagePath).convert('L')
                        img_numpy = np.array(PIL_img,'uint8')
                        name = os.path.split(imagePath)[-1].split(".")[0]
                        id = int(os.path.split(imagePath)[-1].split(".")[1])
                        faceSamples.append(img_numpy)
                        ids.append(id)
                    return faceSamples,ids
                faces,ids = getImagesAndLabels('dataset')
                recognizer.train(faces, np.array(ids))
                recognizer.write('trainer/trainer.yml')

                cursor.execute("INSERT INTO user VALUES ('"+userid+"', '"+voterid+"', '"+name+"', '"+phone+"', '"+address+"')")
                connection.commit()

                return render_template('adduser.html', msg='Successfully user added')
            else:
                return render_template('adduser.html', msg='Entered wrong otp')
    
    return render_template('adduser.html')


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        voterid = request.form['voterid']
        name = request.form['name']

        cursor.execute("delete from user where voterid = '"+voterid+"' and name = '"+name+"'")
        connection.commit()

        if os.listdir('dataset'):
            import cv2
            import numpy as np
            from PIL import Image
            #recognizer = cv2.face.createLBPHFaceRecognizer()
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            def getImagesAndLabels(path):
                imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
                faceSamples=[]
                ids = []
                for imagePath in imagePaths:
                    PIL_img = Image.open(imagePath).convert('L')
                    img_numpy = np.array(PIL_img,'uint8')
                    Name = os.path.split(imagePath)[-1].split(".")[0]
                    if Name == name:
                        os.remove(imagePath)
                    else:
                        id = int(os.path.split(imagePath)[-1].split(".")[1])
                        faceSamples.append(img_numpy)
                        ids.append(id)
                return faceSamples,ids
            faces,ids = getImagesAndLabels('dataset')
            recognizer.train(faces, np.array(ids))
            recognizer.write('trainer/trainer.yml')

            return render_template('deleteuser.html', msg='user deleted succesfully')
        return render_template('deleteuser.html', msg='user deleted succesfully')
    return render_template('deleteuser.html')

@app.route('/add')
def add():
    return render_template('adduser.html')

@app.route('/voterlist')
def voterlist():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    if result:
        return render_template('voterlist.html', result=result)
    else:
        return render_template('voterlist.html', msg='user not found')

@app.route('/Delete')
def Delete():
    return render_template('deleteuser.html')

@app.route('/anounce')
def anounce():
    return render_template('anounce.html')

@app.route('/hold')
def hold():
    con = sqlite3.connect('user_data.db')
    cr = con.cursor()
    cr.execute("select * from voting")
    result = cr.fetchall()
    print(result)
    if result:
        f = open('Result.txt', 'w')
        f.write('hold')
        f.close()
        return render_template('anounce.html', msg = 'result hold')
    else:
        return render_template('anounce.html',  msg = 'voting proccess not yet started')

@app.route('/result')
def result():
    con = sqlite3.connect('user_data.db')
    cr = con.cursor()
    cr.execute("select * from voting")
    result = cr.fetchall()
    print(result)
    if result:
        f = open('Result.txt', 'w')
        f.write('announced')
        f.close()
        return render_template('anounce.html', msg = 'result anounced')
    return render_template('anounce.html',  msg = 'voting proccess not yet started')

@app.route('/display')
def display():
    if os.path.exists('Result.txt'):
        f = open('Result.txt', 'r')
        num = f.readline()
        f.close()

        if num == 'hold':
            return render_template('display.html', result = 'result is hold')
        else:
            con = sqlite3.connect('user_data.db')
            cr = con.cursor()
            cr.execute("select * from voting")
            result = cr.fetchall()
            print(result)
            if result:
                List = []
                for row in result:
                    List.append(row[0])
                print(List)
                
                counter = 0
                num = List[0]

                for i in List:
                    curr_frequency = List.count(i)
                    if(curr_frequency > counter):
                        counter = curr_frequency
                        num = i
                print(num)

                parties = []
                counts = []
                from collections import Counter
                n = Counter(List)
                for m in n:
                    parties.append(m)
                    counts.append(n[m])

                return render_template('display.html', result = 'Winner is {}'.format(num), parties=parties, counts=counts)
            else:
                return render_template('display.html', result = 'result not yet anounced')
    return render_template('display.html', result = 'result not yet anounced')


@app.route('/getotp')
def getotp():
    import random
    number = random.randint(1000,9999)
    number = str(number)
    print(number)
    f = open('OTP.txt', 'w')
    f.write(number)
    f.close()
    bot = telepot.Bot("5505770046:AAHZ00lFDyhh9AL_r7XFrzKaqDT2LWp52V4")
    bot.sendMessage("1388858613", str(number))
    return jsonify('otp sent')

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        otp = int(request.form['otp'])

        f = open('OTP.txt', 'r')
        otp1 = f.readline()
        otp1 = int(otp1)
        f.close()

        if otp == otp1:
            return render_template('userlog.html', msg1='verification successfull')
        else:
            return render_template('userlog.html', msg='entered wrong otp')
            
@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
