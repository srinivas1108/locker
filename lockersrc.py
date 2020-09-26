import hashlib,random
from time import ctime
import smtplib

from flask_ngrok import run_with_ngrok
from flask import Flask,render_template
users={}
usernames=set()
loc={}
frnds={}
forgotpassword={}
rec={}
sent={}
savedtext={}
frndrqst={}
class Register(object):
    def __init__(self,app):
        self.app=app
    def signup(self,username,password,mail,location):
        hash=hashlib.md5(password.encode())
        if username not in users:
            try:
                if loc[location]:
                    loc[location].append(username)
            except:
                loc[location]=[username]
            users.update({username:[hash.hexdigest()]})
            users[username].append(mail)
            users[username].append(location)
            return True
        else:
            return False
    def login(self,username,password):
        hash=hashlib.md5(password.encode())
        if username in users:
            if users[username][0]==hash.hexdigest():
                return True
            else:
                return False
        else:
            return None
    def login1(self,username,password,matter):
        hash=hashlib.md5(password.encode())
        if username in users:
            if users[username][0]==hash.hexdigest():
                users[username].append(matter+'  at  '+ctime())
                return True
            else:
                return False
        else:
            return None
    def otp(self):
        l=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        otp=''
        for i in range(4):
            otp+=random.choice(l)
        return otp
    
app = Flask(__name__)

userobj = Register(app) #starts app instance
run_with_ngrok(app)   #starts ngrok when the app is run

@app.route("/")#home page
def index():
    #return "<html><head></head><body><h1>signup</h1><form>Username : <input type='text'  name='use'><label for='password'>Password : </label><input type='password' id='owd' name='password'><button type='submit' value='submit'></form></body></html>"
    #return '<!DOCTYPE HTML><html><head><body style=background-color:lightgreen;><h1 style=color:white;>LOCKER  🔐  </h1></head><body> <form><table><tr><td>>ereq qaqmqe :</td><td><input type="text"></td></tr><tr><td>Password :</td><td><input type="password"></td></tr><tr><td>Email :</td><td><input type="email"></td></tr><tr><td><input type="submit" value="Submit"></td></tr></table></form></body></html>'
    #return '<html><head><h1>locker</h1></head><body><table><tr><td> Name : </td><td><input type="text"></td></tr><button onclick=location.replace("/signup/<username>/<password>/location")>click me</button></body></html>'
    return "<body style=background-color:lightgreen;><h1 style=color:white;>LOCKER  🔐  </h1><ul><b><li>FOR SIGNUP : /signup/username/password/mail/location</li><li>FOR LOGIN : /login/username/password</li></b></ul><p style=color:blue;>PROTECT YOUR  IMPORTANT TEXT AND DATA HERE AND MAKE FRIENDS!!!</P></body>"

@app.route("/signup/<username>/<password>/<mail>/<location>")  #signup
def reg(username,password,mail,location):
  c=userobj.signup(username,password,mail,location)
  if c:
      toaddr=users[username][1]
      subject='REGISTRATION SUCESSFUL'
      message='Thank you {} for registering LOCKER. Here you can save your important data and text here securely and also can make friends who use LOCKER.'.format(username)
      content='subject: {}\n\n{}'.format(subject,message)
      mail=smtplib.SMTP('smtp.gmail.com',587)
      mail.ehlo()
      mail.starttls()
      mail.login('lockertext1@gmail.com','lockertext@123')
      mail.sendmail('lockertext1@gmail.com',toaddr,content)
      mail.close()
      return "<body style=background-color:powderblue;><h1 style=color:white;>{} successfully registered 😎  .. Login using login/username/password </h1></body>".format(username)
  else:
      return '<body style=background-color:powderblue;><h1 style=color:red;>username-{} already exists.. Try with different one..</h1></body>'.format(username)
@app.route("/login/<username>/<password>/")#routing for login
def login(username,password):
    auth=userobj.login(username,password)
    if auth:
        return '<body style=background-color:lightgreen><h1 style=color:white;>LOGIN  SUCCESSFUL  👍  </h1><h2 style=color:white;>THINGS TO KNOW TO USE THIS API..</h2><ul><li>FOR  SAVING  THE  TEXT  :  /login/username/password/textuwanttosave</li><li>TO  GET  OTP  FOR  UNLOCKING  YOUR  SAVED  TEXT  :  /login/username/password/unlock</li><li>TO  VIEW  THE  SAVED  TEXT  :  /login/username/password/saved/otp</li><li>TO  VIEW  THE  USERS  :  /login/username/password/users</li><li>TO  VIEW  THE  USERS  IN  YOUR  LOCALITY  :  /login/username/password/users/location</li><li>TO  SEND  THE  FRIEND  REQUESTS  :  /login/username/password/friendrequest/friendname</li><li>TO  ACCEPT  THE  FRIEND  REQUEST  :  /login/username/password/acceptfriendrequest/frndname/otp</li><li>TO  VIEW  YOUR  FRIENDS  :  /login/username/password/friends</li><li>TO  SEND  MESSAGE  TO  FRIENDS  :  /login/username/password/message/ur message/frndname</li><li>TO  VIEW  THE  RECEIVED  MESSAGES  :  /login/username/password/inbox</li><li>TO  VIEW  THE  SENT  MESSAGES:  /login/username/password/sent</li><li>FORGOT PASSWORD : /username/forgotpassword</li></ul><p style=color:blue;>Note 1 ✍️ : Saved data in LOCKER are seperated by * for better understanding</p><p style=color:blue;>Note 2 ✍️:To view the saved data in LOCKER..You need to enter otp sent to your mail...When anyuser send friend request to you.You will get a mail containg the url to accept the friendrequest..</p><p style=color:blue;> Note 3 ✍️ : when you request for forgot password, an email containing otp and url is sent to change password or reset password..</p></body>'
#'<body style=background-color:lightgreen><h1 style=color:white;>LOGIN  SUCCESSFUL  👍  </h1><h2 style=color:white;>THINGS TO KNOW TO USE THIS API..</h2><ul><li>FOR  SAVING  THE  TEXT  :  /login/username/password/textuwanttosave</li><li>TO  GET  OTP  FOR  UNLOCKING  YOUR  SAVED  TEXT  :  /login/username/password/unlock</li><li>TO  VIEW  THE  SAVED  TEXT  :  /login/username/password/saved/otp</li><li>TO  VIEW  THE  USERS  :  /login/username/password/users</li><li>TO  VIEW  THE  USERS  IN  YOUR  LOCALITY  :  /login/username/password/users/location</li><li>TO  SEND  THE  FRIEND  REQUESTS  :  /login/username/password/friendrequest/friendname</li><li>TO  ACCEPT  THE  FRIEND  REQUEST  :  /login/username/password/acceptfriendrequest/frndname/otp</li><li>TO  VIEW  YOUR  FRIENDS  :  /login/username/password/friends</li><li>TO  SEND  MESSAGE  TO  FRIENDS  :  /login/username/password/message/ur message/frndname</li><li>TO  VIEW  THE  RECEIVED  MESSAGES  :  /login/username/password/inbox</li><li>TO  VIEW  THE  SENT  MESSAGES:  /login/username/password/sent</li><li>FORGOT PASSWORD : /username/forgotpassword</li></ul><p style=color:blue;>Note 1 ✍️ : Messages and saved text are seperated by * to avoid collision between one message (or text) and another message(or text)</p><p style=color:blue;>Note 2 ✍️:To view the saved data in locker..You need to enter otp sent to your mail...When anyuser send friend request to you.You will get a mail containg the url to accept the friendrequest..</p><p style=color:blue;> Note 3 ✍️ : when you request for forgot password, an email containing otp and url is sent to change password or reset password..</p> </body>'
    elif auth==None:        
        return '<body style=background-color:powderblue;><h2 style=color:white;>YOU DID NOT REGISTERED...KINDLY REGISTER BY  :  /signup/username/password/mail/location</h2></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED  👎 TRY AGAIN!!</h1></body>'

@app.route("/login/<username>/<password>/<matter>") #save text
def login1(username,password,matter):
  auth = userobj.login1(username,password,matter)
  if auth:
      return '<body style=background-color:powderblue;><h1 style=color:white;>YOUR TEXT SAVED SECURELY : )</h1></body>'
  else:
      return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG PASSWORD!  👎 TRY AGAIN!!</h1></body>'

@app.route('/login/<username>/<password>/unlock')#otp to view the saved text
def sri(username,password):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        ot=userobj.otp()
        try:
            if savedtext[username]:
                savedtext[username].append(ot)
        except:
            savedtext[username]=[ot]
        toaddr=users[username][1]
        subject='OTP'
        message='your one time password to unlock your saved text in locker is {}'.format(ot)
        content='subject: {}\n\n{}'.format(subject,message)
        mail=smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('lockertext1@gmail.com','lockertext@123')
        mail.sendmail('lockertext1@gmail.com',toaddr,content)
        mail.close()
        return '<body style=background-color:powderblue;><h1 style=color:white;>OTP is sent to your mail 📧 kindly enter provided OTP to unlock the locked text or data...To view the saved text go to  :  /login/username/password/saved/otp</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 TRY AGAIN!!</h1></body>'
@app.route('/login/<username>/<password>/saved/<otp>')#to view the saved text
def srin(username,password,otp):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest() and len(users[username][3:])!=0 and savedtext[username][-1]==otp:
        return '<body style=background-color:lightgreen;><h1 style=color:white;>YOUR LOCKER</h1><h2>{}</h2></body>'.format(' * '.join(users[username][3:]))
    elif users[username][0]==s.hexdigest() and len(users[username][3:])==0 and savedtext[username][-1]==otp:
        return '<body style=background-color:powderblue;><h1  style=color:white>YOUR ARE NOT SAVED ANY TEXT UNTIL NOW</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎  KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
@app.route("/login/<username>/<password>/users")#to view the users
def data(username,password):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        for i in users.keys():
            usernames.add(i)
        return '<body style=background-color:powderblue;><h1 style=color:white;>USERS USING LOCKER</h1><h2>{}</h2></body>'.format(' , '.join(usernames))
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED  👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'

        
@app.route('/login/<username>/<password>/friendrequest/<frndname>')#to send the friend request
def data2(username,password,frndname):
    s=hashlib.md5(password.encode())
    if frndname in users and frndname!=username:
        if users[username][0]==s.hexdigest():
            ot=userobj.otp()
            try:
                if frndrqst[username]:
                    frndrqst[username].update({frndname:ot})
            except:
                frndrqst[username]={frndname:ot}
            
            toaddr=users[frndname][1]
    
            subject='FRIEND REQUEST'
            message='{} wants to be your friend. To accept friend request go to  :/login/username/password/acceptfriendrequest/{}/{}'.format(username,username,ot)
            content='subject: {}\n\n{}'.format(subject,message)
            mail=smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('lockertext1@gmail.com','lockertext@123')
            mail.sendmail('lockertext1@gmail.com',toaddr,content)
    
            mail.close()
            return '<body style=background-color:lightyellow;><h1 style=color:blue;>Friend request is sent through an email 📧 to {} .. </h1></body>'.format(frndname)
        
        else:
            return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED.KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
    elif username==frndname:
        return '<body style=background-color:powderblue;><h1 style=color:red;>YOU CAN NOT SEND FRIEND REQUEST TO YOURSELF..</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>USERNAME NOT FOUND.....</h1></body>'


@app.route('/login/<username>/<password>/acceptfriendrequest/<frndname>/<otp>')#to accept the friend request
def data3(username,password,frndname,otp):
    
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest() and otp==frndrqst[frndname][username]:
        try:
            if frnds[username]:
                frnds[username].append(frndname)
                try:
                    if frnds[frndname]:
                        frnds[frndname].append(username)
                except:
                    frnds[frndname]=[username]
                
        except:
            frnds[username]=[frndname]
            try:
                if frnds[frndname]:
                    frnds[frndname].append(username)
            except:
                frnds[frndname]=[username]
            
        toaddr=users[frndname][1]
    
        subject='FRIEND REQUEST ACCEPTED'
        
        message='Your friend request is accepted by {}'.format(username)
        content='subject: {}\n\n{}'.format(subject,message)
        mail=smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('lockertext1@gmail.com','lockertext@123')
        mail.sendmail('lockertext1@gmail.com',toaddr,content)
    
        mail.close()
        return '<body style=background-color:lightyellow;><h1 style=color:blue>Friend request accepted !! Now you and {} are friends 🤝  </h1></body>'.format(frndname)
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED.KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'


@app.route('/login/<username>/<password>/users/<locality>')#to view the users present in ur locality
def data4(username,password,locality):
     s=hashlib.md5(password.encode())
     if users[username][0]==s.hexdigest():
         if locality in loc:
             return '<body style=background-color:powderblue;><h1 style=color:white;>  LOCKER  users  in {}</h1><h2>{}</h2></body>'.format(locality,(' , '.join(loc[locality])))
         else:
            return '<body style=background-color:powderblue;><h1 style=color:red;>NO USERS FOUND IN THIS LOCALITY..</h1></body>'
     else:
         return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'


@app.route('/login/<username>/<password>/friends/')#to view your friends
def data5(username,password):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        try:
            if frnds[username]:
                return '<body style=background-color:powderblue;><h1 style=color:white;>FRIENDS</h1><h2>{}</h2></body>'.format(' ,'.join(frnds[username]))
        except:
            return '<body style=background-color:powderblue;><h1 style=color:white; >NO FRIENDS YET!!</h1><h2> MAKE FRIENDS BY SENDING FRIEND REQUEST TO ANY OF THE USERS USING THIS API...TO SEND A FRIEND REQUEST GO TO  :  login/username/password/friendrequest/friendname</h2></body>'
    else:
         return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
@app.route('/login/<username>/<password>/message/<message>/<friendname>/')
def data6(username,password,message,friendname):#to send message
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        try:
            if friendname in frnds[username]:
                try:
                    if sent[username]:
                        sent[username].append('To '+friendname+' :' +message+' at   '+ctime())
                        try:
                            if rec[friendname]:
                                rec[friendname].append('From '+username+' : '+message+' at  '+ctime())
                        except:
                            rec[friendname]=['From '+username+' : '+message+' at  '+ctime()]
                except:
                    sent[username]=['To '+friendname+' : '+message+' at  '+ctime()]
                    try:
                        if rec[friendname]:
                            rec[friendname].append('From'+username+' :'+message+' at  '+ctime())
                    except:
                        rec[friendname]=['From '+username+' : '+message+' at  '+ctime()]
                        
                return '<body style=background-color:powderblue;><h1 style=color:white;>Message sent to {}</h1></body>'.format(friendname)
            else:
                return '<body style=background-color:powderblue;><h1 style=color:white;>You can not send message to {} since he or she is not your friend:( </h1><h2>To make {} as friend send friend request to {} BY:/login/username/password/friendrequest/friendname</h2></body>'.format(friendname,friendname,friendname)
        except:
            return '<body style=background-color:powderblue;><h1 style=color:white;>YOUR FRIENDS LIST IS EMPTY</h1><h2>You can not send message to {} since he or she is not your friend:( To make {} as friend send friend request to {} BY:/login/username/password/friendrequest/friendname</h2></body>'.format(friendname,friendname,friendname) 
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
@app.route('/login/<username>/<password>/inbox')#to view inbox
def data7(username,password):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        try:
            if rec[username]:
                return '<body style=background-color:powderblue;><h1 style=color:white;>INBOX</h1><h2>{}</h2></body>'.format('     *     '.join(rec[username]))
        except:
            return '<body style=background-color:powderblue;><h1>No messages for you!!</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
@app.route('/login/<username>/<password>/sent')#to view sent
def data8(username,password):
    s=hashlib.md5(password.encode())
    if users[username][0]==s.hexdigest():
        try:
            if sent[username]:
                return '<body style=background-color:powderblue;><h1 style=color:white;>SENT MESSAGES</h1><h2>{}</h2></body>'.format('     *     '.join(sent[username]))
        except:
            return '<body style=background-color:powderblue;><h1>No sent messages!!</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:red;>WRONG DETAILS PROVIDED 👎 KINDLY CHECK AND TRY ONCE AGAIN!</h1></body>'
@app.route('/<username>/forgotpassword')#forgot password
def data9(username):
    if username in users:
        ot=userobj.otp()
        try:
            if forgotpassword[username]:
                forgotpassword[username]=ot
        except:
            forgotpassword[username]=ot
        toaddr=users[username][1]
        subject='PASSWORD RESET!'
        message='your one time password to change your password is {} . To change password go to: username/changepassword/otp/newpassword'.format(ot)
        content='subject: {}\n\n{}'.format(subject,message)
        mail=smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('lockertext1@gmail.com','lockertext@123')
        mail.sendmail('lockertext1@gmail.com',toaddr,content)
        mail.close()
        return '<body style=background-color:powderblue;><h1 style=color:white;>DONT WORRY EVEN IF YOUR PASSWORD WAS LOST..OTP AND URL IS SENT TO YOUR MAIL..VERIFY IT TO  GAIN ACCESS TO LOCKER..</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:white;>USERNAME NOT FOUND!!!</h1></body>'
@app.route('/<username>/changepassword/<otp>/<newpassword>')
def data10(username,otp,newpassword):
    if username in users:
        if forgotpassword[username]==otp:
            s=hashlib.md5(newpassword.encode())
            users[username][0]=s.hexdigest()
            return '<body style=background-color:powderblue;><h1 style=color:white;>YOUR PASSWORD WAS UPDATED!!LOGIN WITH NEW PASSWORD!</h1></body>'
        else:
            return '<body style=background-color:powderblue;><h1 style=color:white;>WRONG OTP PROVIDED!! CHECK AGAIN!!</h1></body>'
    else:
        return '<body style=background-color:powderblue;><h1 style=color:white;>USERNAME NOT FOUND!!!</h1></body>'
    

app.run()
