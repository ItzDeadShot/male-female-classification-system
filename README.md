# male-female-classification-system
System to classify male and female.


To run the application, download Docker from [here](https://www.docker.com/products/docker-desktop/).

Then run the following command in the same directory as this application to build docker image:

`docker build --tag python-docker .`

Now you can confirm if the docker image is present:

`docker images`
```
REPOSITORY        TAG       IMAGE ID       CREATED             SIZE           
python-docker     latest    ab18451537b4   About an hour ago   3.7GB
reborntc/webmap   latest    9efc6c57afaa   2 years ago         1.84GB
```

Once you see python-docker image in images, you can execute the following commad to run the docker:

`docker run --name=genclass -d -p 5000:5000 python-docker`

Now you can access the web applicaton from [127.0.0.1](http://127.0.0.1:5000)
