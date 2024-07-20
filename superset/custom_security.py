from flask import redirect, g, flash, request
from flask_appbuilder.security.views import AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_login import login_user
from sqlalchemy import create_engine, text
import sys
import os
from dotenv import load_dotenv
import jwt
import time

load_dotenv()


url = os.getenv('url')

engine = create_engine(url)

class SupersetAuth:
    def __init__(self, id, token, username, consumed, creationDate, expirationDate, consumedDate, userId):
        self.id = id
        self.token = token
        self.username = username
        self.consumed = consumed
        self.creationDate = creationDate
        self.expirationDate = expirationDate
        self.consumedDate = consumedDate
        self.userId = userId

class CustomAuthDBView(AuthDBView):
    login_template = 'appbuilder/general/security/login_db.html'

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        
        authsuccess = False
        usernameFromPath = ''
        token = ''
        redirect_url = self.appbuilder.get_url_for_index
        if request.args.get('redirect') is not None:
            redirect_url = request.args.get('redirect') 
        if request.args.get('username') is not None:
            usernameFromPath = request.args.get('username')
            user = self.appbuilder.sm.find_user(username=usernameFromPath)
            sys.stdout.flush()
        if request.args.get('token') is not None:
            token = request.args.get('token')
        
        if usernameFromPath != '':
            try:
                conn = engine.connect()
                result = conn.execute(text('SELECT * FROM superset_auth WHERE username=:username and token=:token'), {'username': usernameFromPath, 'token': token})

                fromDb = result.fetchone()
                if fromDb:
                    supersetAuth = SupersetAuth(*fromDb)
                    if supersetAuth.consumed:
                        flash('Invalid token', 'warning')
                        return super().login()
                    
                    data = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])

                    if data['username'] == usernameFromPath and data['exp'] > time.time():
                        # conn.execute(text('UPDATE superset_auth SET consumed = true WHERE username = :username AND token = :token'), {'username': usernameFromPath, 'token': token})
                        print('Token is valid')
                        sys.stdout.flush()
                        authsuccess = True
            except Exception as error:
                print('Error at line 68', str(error))
                sys.stdout.flush()
            finally:
                if conn:
                    print('Closing connection')
                    sys.stdout.flush()
                    conn.close()
        else:
            return super(CustomAuthDBView,self).login()

        if g.user is not None and g.user.is_authenticated and not authsuccess:
            return redirect(redirect_url)
        
        if authsuccess:
            flash('Admin auto logged in', 'success')
            login_user(user, remember=False)
            print('User logged in')
            sys.stdout.flush()
            return redirect(self.appbuilder.get_url_for_index)
        else:
            flash('Auto Login Failed', 'warning')
            return super().login()

class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)

