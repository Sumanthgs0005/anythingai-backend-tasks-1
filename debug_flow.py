import os
os.environ['PYTEST_CURRENT_TEST'] = 'debug_flow'
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

r1 = client.post('/api/v1/auth/register', json={'email':'flow@example.com', 'password':'pass123'})
print('register status', r1.status_code, r1.text)
if r1.status_code == 200:
    token = r1.json().get('access_token')
    # decode token
    from jose import jwt
    from app.auth import SECRET_KEY, ALGORITHM
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print('token payload', payload)
    # check DB for user id
    from app.database import SessionLocal
    db = SessionLocal()
    uid = payload.get('sub')
    u = db.execute('SELECT id, email FROM users WHERE id=?', (uid,)).fetchone()
    print('db user for sub', u)
    headers = {'Authorization': f'Bearer {token}'}
    r2 = client.post('/api/v1/tasks/', headers=headers, json={'title':'t','description':'d'})
    print('create task', r2.status_code, r2.text)
else:
    print('register failed')
