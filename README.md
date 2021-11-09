# Test Users Service

### Development
```
sudo docker run \
  -it \
  --name users --rm \
  -p 5000:5000 --net percepthor \
  -v /home/ermiry/Documents/Work/users-service:/home/users \
  -v /home/ermiry/Documents/Work/keys:/home/keys \
  -e RUNTIME=development \
  -e PORT=5000 \
  -e CERVER_RECEIVE_BUFFER_SIZE=4096 -e CERVER_TH_THREADS=4 \
  -e CERVER_CONNECTION_QUEUE=4 \
  -e MONGO_APP_NAME=users -e MONGO_DB=percepthor \
  -e MONGO_URI=mongodb://users:password@192.168.100.39:27017/percepthor \
  -e PRIV_KEY=/home/keys/key.key -e PUB_KEY=/home/keys/key.pub \
  itpercepthor/users-service:development /bin/bash
```

## Routes

### Main

#### GET /api/users
**Access:** Public \
**Description:** Users service top level route \
**Returns:**
  - 200 on success

#### GET /api/users/version
**Access:** Public \
**Description:** Returns users service current version \
**Returns:**
  - 200 and version's json on success

#### GET /api/users/auth
**Access:** Private \
**Description:** Used to test if JWT keys work correctly \
**Returns:**
  - 200 on success
  - 401 on failed auth
  - 500 on server error

### Auth

#### POST /api/users/login
**Access:** Public \
**Description:** Performs login into user's account and generates a JWT token \
**Returns:**
  - 200 on success
  - 400 on bad request
  - 404 on not found
  - 500 on server error

#### POST /api/users/register
**Access:** Public \
**Description:** Creates a new user account and generates a JWT token \
**Returns:**
  - 200 on success
  - 400 on bad request
  - 500 on server error
