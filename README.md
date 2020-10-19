
How to setup the project on Linux

---
Install Docker

https://docs.docker.com/engine/install/ubuntu/


- uninstall older versions on Docker
```
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```
	
- install Docker using repository
```
$ sudo apt-get update
```

```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

```
 $ sudo apt-get update
```

```
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

- verify installation
```
$ sudo docker run hello-world
```


---
Build the system from image

- go to directory which docker file is located(Django folder)

- build
```
$ sudo docker build --tag restaurantratingsystem .
```

---
- Install docker-compose
```
$ sudo apt-get install docker-compose
```

---
Run the project

- go to root directory that docker-compose file is located
```
$ sudo docker-compose up
```

---
Change the docker-compose reference version format if some issue occurred

- docker-compose file located in root directory
- in the first line  you can see something like " version: "3" "
- change it to compatible version with your docker engine
	- ex :- change it as " version: "3.3" " 


---
Migrating DB models

- enter to python shell via docker
```
$ sudo docker exec -it dj bash
```

- migrate 
```
$ python manage.py migrate
```

---
Create super user for Django

https://stackoverflow.com/questions/18503770/how-to-create-user-from-django-shell

- enter to python shell via docker
```
$ sudo docker exec -it dj bash
```

- create super user
```
$python manage.py createsuperuser
```

---
Check the system

- in browser go to - https://127.0.0.1:8080
