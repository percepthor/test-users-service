# Test Users Service

### Development
```
sudo docker run \
  -it \
  --name users --rm \
  -p 5000:5000 --net percepthor \
  -v /home/ermiry/Documents/Work/users-service:/home/users \
  -e RUNTIME=development \
  -e PORT=5000 \
  -e CERVER_RECEIVE_BUFFER_SIZE=4096 -e CERVER_TH_THREADS=4 \
  -e CERVER_CONNECTION_QUEUE=4 \
  itpercepthor/users-service:development /bin/bash
```

## Routes

### Main

#### GET /api/users
**Access:** Public \
**Description:** Users top level route \
**Returns:**
  - 200 on success

#### GET /api/users/version
**Access:** Public \
**Description:** Returns users service current version \
**Returns:**
  - 200 and version's json on success
