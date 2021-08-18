#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
from config.postgresConfig import *

@app.route("/regis/usercafe",methods=["POST"])
def regis_add_usercafe():
    try:
        data = request.json
        if 'username' in data and 'password' in data and 'repassword' in data and 'role' in data:
            conn = connectToDB()
            cursor = conn.cursor()
            username = data['username']
            if len(username) < 8 or  len(username) > 20:
                result = {'status':"ER",'errorMessage':"username be between 8 and 20 characters"}
                return jsonify(result),200
            password = data['password']
            repassword = data['repassword']
            if password != repassword:
                result = {'status':"ER",'errorMessage':"Password not match!!!"}
                return jsonify(result),403

            hax_user = hashlib.md5(username.encode())
            user_id = hax_user.hexdigest()
            hax_password = hashlib.md5(password.encode())
            password_encode = hax_password.hexdigest()
            role = data['role']

        
            try:
                sqlselect = 'SELECT * FROM "user_cafe" WHERE user_id = %s'
                cursor.execute(sqlselect,(user_id,))
                data = cursor.fetchall()
            except Exception as e:
                current_app.logger.info(str(e))
                data = []
            if data != []:
                columns = [column[0] for column in cursor.description]
                result = toJson(data,columns)
                result = result[0]
                result = {"status":"ER","message":"user dupclicate"}
                return jsonify(result),403
                
            else:
                try:
                    sql = """
                        INSERT INTO "user_cafe" (user_id, username, password, role) 
                        VALUES (%s,%s,%s,%s)
                        """
                    cursor.execute(sql,(user_id,username,password_encode,role))
                    conn.commit()
                    result = {"status":"OK","message":"Insert data success"}
                    return jsonify(result),200
                except Exception as e:
                    result = {"status":"ER","errorMessage":str(e),"errorCode":"ER02"}
                    return jsonify(result),500
                finally:
                    conn.close()
        else:
            result = {"status":"ER","errorMessage":"Data Not Complete","errorCode":"ER01"}
            return jsonify(result),403

    except Exception as e:
        result = {"status":"ER","errorMessage":str(e),"errorCode":"ER999"}
        return jsonify(result),500