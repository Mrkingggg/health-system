
def test_hello(test_client):
    response = test_client.get('/api/users/hello')
    assert response.status_code == 200
    assert b"hello world" in response.data

def test_add_user(test_client, init_database):
    
    response = test_client.post('/api/users/add', json={
        'username': 'john',
        'email': 'john@example.com',
        'dob': '1990-01-01',
        'fullname': 'John Doe',
        'password': '123456',
        'gender': 'male'
    })
    assert response.status_code == 201

    
    response = test_client.post('/api/users/add', json={
        'username': 'john2'
    })
    assert response.status_code == 400

    
    response = test_client.post('/api/users/add', json={
        'username': 'john',
        'email': 'johnny@example.com',
        'dob': '1990-01-02',
        'fullname': 'Johnny Doe',
        'password': 'abcdef',
        'gender': 'male'
    })
    assert response.status_code == 400

   
    response = test_client.post('/api/users/add', json={
        'username': 'jane',
        'email': 'jane@example.com',
        'dob': '01-01-1990',
        'fullname': 'Jane Doe',
        'password': '123456',
        'gender': 'female'
    })
    assert response.status_code == 400

def test_change_user_role(test_client, init_database):
    
    response = test_client.post('/api/users/add', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'dob': '1990-02-02',
        'fullname': 'Test User',
        'password': 'testpassword',
        'gender': 'male'
    })
    user_id = response.json['userId']

    
    response = test_client.put(f'/api/users/changeRole', json={
        'userId': user_id,
        'newRoles': [1]
    })
    assert response.status_code == 200


    response = test_client.put('/api/users/changeRole', json={
        'userId': 99999,
        'newRoles': [1]
    })
    assert response.status_code == 404

  
    response = test_client.put('/api/users/changeRole', json={
        'userId': user_id
    })
    assert response.status_code == 400



def test_send_notification(test_client, init_database):
    
    response = test_client.post('/api/notifications/send', json={
        'userId': 1,
        'msg': 'Test Message'
    })
    assert response.status_code == 202

    
    response = test_client.post('/api/notifications/send', json={
        'userId': 999,
        'msg': 'Test Message'
    })
    assert response.status_code == 400

    
    response = test_client.post('/api/notifications/send', json={
        'userId': 1
    })
    assert response.status_code == 400


def test_login(test_client, init_database):
   
    response = test_client.post('/api/auth/login', json={
        'username': 'existinguser',
        'password': 'correctpassword',
        'role': 1
    })
    assert response.status_code == 200

   
    response = test_client.post('/api/auth/login', json={
        'username': 'existinguser',
        'password': 'wrongpassword',
        'role': 1
    })
    assert response.status_code == 401
    assert "incorrect password" in response.json['error']

   
    response = test_client.post('/api/auth/login', json={
        'username': 'nonexistentuser',
        'password': 'password',
        'role': 1
    })
    assert response.status_code == 400
    assert "invalid username" in response.json['bad request']

def test_browse_patients(test_client, init_database):
    response = test_client.get('/api/MP/browsePatient')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # 应返回一个列表

def test_make_appointment(test_client, init_database):
    
    response = test_client.post('/api/patient/makeAppointment', json={
        'doctorId': 2,
        'patientId': 1,
        'appointment_time': '2023-10-01T15:00:00'
    })
    assert response.status_code == 200
    assert "appointment scheduled" in response.json['message']

    
    response = test_client.post('/api/patient/makeAppointment', json={
        'doctorId': 2,
        'patientId': 1,
        'appointment_time': '10-01-2023 15:00'
    })
    assert response.status_code == 500

def test_add_measurement(test_client, init_database):
    
    response = test_client.post('/api/MP/addMeasureData', json={
        'userId': 1,
        'deviceId': 1,
        'value': '120',
        'measuretime': '2023-10-01T15:00:00',
        'measuretype': 'blood_pressure'
    })
    assert response.status_code == 200
    assert "add measurement succeed" in response.json['message']

    
    response = test_client.post('/api/MP/addMeasureData', json={
        'userId': 1
    })
    assert response.status_code == 400
    assert "Missing info" in response.json['error']


def test_register_device(test_client, init_database):
    
    response = test_client.post('/api/admin/RegisDevice', json={
        'manufactor': 'TestCorp',
        'devType': 'Heart Monitor',
        'status': 1,
        'unit': 'bpm'
    })
    assert response.status_code == 200
    assert "Device registered successfully" in response.json['message']

    
    response = test_client.post('/api/admin/RegisDevice', json={
        'manufactor': 'TestCorp'
    })
    assert response.status_code == 400
    assert "missing information" in response.json['error']


def test_view_device(test_client, init_database):
    
    response = test_client.get('/api/admin/viewDevice')
    assert response.status_code == 200
    
    assert isinstance(response.json, list)


def test_delete_device(test_client, init_database):
   
    response = test_client.delete('/api/admin/deldev/1')
    assert response.status_code == 200
    assert "Device deleted successfully" in response.json['message']

    
    response = test_client.delete('/api/admin/deldev/999')
    assert response.status_code == 400
    assert "device does not exist" in response.json['bad request']

def test_change_device_status(test_client, init_database):
    
    response = test_client.put('/api/admin/1/chgstatus', json={'status': 0})
    assert response.status_code == 200
    assert "Device status updated" in response.json['message']

    
    response = test_client.put('/api/admin/999/chgstatus', json={'status': 0})
    assert response.status_code == 404
    assert "Device not found" in response.json['error']


def test_view_appointment(test_client, init_database):
    
    response = test_client.get('/api/MP/view_appointment?doctorId=1')
    assert response.status_code == 200
    assert isinstance(response.json, list)  

    
    response = test_client.get('/api/MP/view_appointment')
    assert response.status_code == 400
    assert "doctor_id not found" in response.json['error']


def test_add_chat_patient(test_client, init_database):
    
    response = test_client.post('/api/MP/add_chat_patient', json={
        'MPid': 1,
        'patientid': 2
    })
    assert response.status_code == 200
    assert "succeed in adding chat patient" in response.json['message']

    
    response = test_client.post('/api/MP/add_chat_patient', json={
        'MPid': 1
    })
    assert response.status_code == 400
    assert "missing info" in response.json['error']


def test_remove_chat_patient(test_client, init_database):
    
    response = test_client.delete('/api/MP/remove_chat_patient?MPid=1&patientid=2')
    assert response.status_code == 200
    assert "delete this chat pair" in response.json['message']

    
    response = test_client.delete('/api/MP/remove_chat_patient?MPid=1&patientid=999')
    assert response.status_code == 404
    assert "No such chat pair" in response.json['error']