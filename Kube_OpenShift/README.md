# Fundamentals of Containers, Kubernetes, and Red Hat OpenShift
_**EDX**_

## Chapter 1 - Getting Started with Container Technology
02/16/2020
- Kubernetes takes care of orchestration, scheduling, and isolation
   - Provides services, scheduling, isolation
- Master/worker architecture
- Pods - 1 or more containers that share resources
   - 1 container/1 pod is common
   - Use services to have a persistent IP address so pods can communicate
- Replication controllers - objects to help scale an application out
- Persistent volumes and claims used to persist data
   - Multiple containers on different hosts share persistent volumes
- OpenShift is a layer built upon containers and Kubernetes
   - Use to create CI/CD pipeline

![master / worker node architecture](./images/master_worker_nodes.png)

- Services allow pods to communicate
- Deployment configurations represent pods created from the same container
  image

![OpenShift technology stack](./images/technology_stack.png)

-----
04/22/2020
- Kubernetes handles orchestration, scheduling, isolation
   - Orchestration - how to get containers to talk to each other
      - Containers are transient, things like IP address can change
      - Kubernetes uses services to manage changing properties
   - Scheduling -
      - Maintain a certain number of container instances
      - Schedule instances based on system load
   - Isolation - prevent container failures from affecting each other
- Kubernetes manages clusters of pods
   - Master node runs commands via ```kube-control```
   - Pods are 1 or more containers that share an IP address
      - Common model is 1 container per pod, but possible to run more in a pod
   - Kube uses services to persist the IP address of a pod
   - Replication controllers scale applications out
   - Persistent volumes persist data
      - Persistent volume claims indicate which volumes a container needs access to
- OpenShift builds on top of Kube & containers
   - Web console - orchestrate & manage container cluster
      - Scale pods
      - Manage role-based access
      - Source image automation
   -

-----
04/26/2020
- Deployment configurations represent a set of pods created from the same container image
   - Helps a lot with rolling updates to base images
- Build configurations
   - Automate build processes for updates to images
- etcd - key value store used by Kubernetes
- Containerized services provided by OS are pods running in the background
- OS comes with all of the Runtimes and xPaaS included - lots of languages and
  API libraries


## Chapter 2 - Creating Containerized Services
04/26/2020

### Building a Development environment with OpenShift
Started an OS project cluster using all of the default settings.  This is a KVM-based
project that took about 15 minutes to completely setup.  I ran the ```minishift start```
command to kick off the project build process, and it provided this information
towards the end of the build process:

```
Creating initial project "myproject" ...
Server Information ...
OpenShift server started.

The server is accessible via web console at:
    https://192.168.42.121:8443/console

You are logged in as:
    User:     developer
    Password: <any value>

To login as administrator:
    oc login -u system:admin
```

I logged into the console as developer/spd95tpl

![The OpenShift web console](./images/OpenShift_web_console.png)

Showing the status of my project:
```
(base) /home/aragorn> minishift status
Minishift:  Running
Profile:    minishift
OpenShift:  Running (openshift v3.11.157)
DiskUsage:  14% of 19G (Mounted On: /mnt/sda1)
CacheUsage: 1.446 GB (used by oc binary, ISO or cached images)
RHSM: 	    Registered
```

Showing the config of my project
```
(base) /home/aragorn> minishift config view
- iso-url                            : file:///home/aragorn/.minishift/cache/iso/minishift-rhel7.iso
- memory                             : 4096
- vm-driver                          : kvm
```

Have to make sure that the Minishift username and password match my credentials for
my Red Hat developer subscription.  I have this setup in my .bashrc.

When I start my project, there is a failure logging on to the subscription manager:
```
-- Registering machine using subscription-manager
   Login to registry.redhat.io in progress . FAIL
   Registration in progress ......... OK [18s]
```

The problem turns out to be a special character I had in my password - probably
"$".  I changed my password to all numbers and letters, and things work fine now.

Once the project VM is running, we can use the OpenShift Command line ```oc```, to
interact with the cluster:
```
(base) /home/aragorn> oc version
oc v3.11.157
kubernetes v1.11.0+d4cacc0
features: Basic-Auth GSSAPI Kerberos SPNEGO

Server https://192.168.42.121:8443
kubernetes v1.11.0+d4cacc0
```

I can log in as the administrator:
```
(base) /home/aragorn> oc login -u system:admin
Logged into "https://192.168.42.121:8443" as "system:admin" using existing credentials.

You have access to the following projects and can switch between them with 'oc project <projectname>':

    default
    kube-dns
    kube-proxy
    kube-public
    kube-system
  * myproject
    openshift
    openshift-apiserver
    openshift-controller-manager
    openshift-core-operators
    openshift-infra
    openshift-node
    openshift-service-cert-signer
    openshift-web-console

Using project "myproject".
```

Make sure that the pods we want running in the default project are actually running:
```
(base) /home/aragorn> oc get pods -n default
NAME                            READY     STATUS      RESTARTS   AGE
docker-registry-1-crzff         1/1       Running     1          45m
persistent-volume-setup-fmnn5   0/1       Completed   0          45m
router-1-qkg6f                  1/1       Running     1          45m
```

We can use the Minishift ssh command to get directly into the Docker machine inside
the myproject VM:
```
(base) /home/aragorn> minishift ssh
[docker@minishift ~]$ docker ps
CONTAINER ID        IMAGE                                                                                                                             COMMAND                  CREATED             STATUS              PORTS               NAMES
e81e4797cb10        registry.access.redhat.com/openshift3/ose-hypershift@sha256:1f7c10e604727bd9d0b88b8a44a7b5ddea4f9b636ec9bcc584ce4aca014607e0      "hypershift experi..."   12 minutes ago      Up 12 minutes                           k8s_operator_openshift-web-console-operator-6d5b8db4f7-d52cg_openshift-core-operators_efbf132e-87c7-11ea-92be-525400b002e3_1
210a378ea3fd        docker.io/openshift/origin-service-serving-cert-signer@sha256:699e649874fb8549f2e560a83c4805296bdf2cef03a5b41fa82b3820823393de    "service-serving-c..."   12 minutes ago      Up 12 minutes                           k8s_operator_openshift-service-cert-signer-operator-6d477f986b-xrd6m_openshift-core-operators_ab366f02-87c7-11ea-92be-525400b002e3_1
20d8d8c3cc25        registry.access.redhat.com/openshift3/ose-hypershift@sha256:1f7c10e604727bd9d0b88b8a44a7b5ddea4f9b636ec9bcc584ce4aca014607e0      "hypershift opensh..."   12 minutes ago      Up 12 minutes                           k8s_apiserver_openshift-apiserver-pxq2j_openshift-apiserver_ab53e813-87c7-11ea-92be-525400b002e3_1
<many more containers ...>
```

There are _more than 30_ containers running in this project, just to start a default
environment.  Note that there are containers running for each of the pods from the
output of the ```oc get pods -n default``` command

### Provisioning a Database Server
Red Hat Container Image Catalog is the place to go for images

- Make sure the myproject minishift VM is up and running
   - ```minishift start```
- Hit the OpenShift web console for this project, and log in as developer/spd95tpl
   - ```https://192.168.42.121:8443/console/```
- ssh into the VM
   - ```minishift ssh```
- Starting up the mysql container from the demo:
   - ```docker run --name mysql-basic -e MYSQL_USER=user1 -e MYSQL_PASSWORD=mypa55 -e MYSQL_DATABASE=items -e MYSQL_ROOT_PASSWORD=r00tpa55 -d mysql:5.6```
   - This will pull the image from Dockerhub, and not the redhat catalog as in the demo.
- Docker exec into the mysql container
   - ```docker exec -it mysql-basic bash```
- Connect to the mysql instance
  ```
  root@24fc29f94092:/# mysql -pr00tpa55
  Warning: Using a password on the command line interface can be insecure.
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  Your MySQL connection id is 2
  Server version: 5.6.48 MySQL Community Server (GPL)

  Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

  Oracle is a registered trademark of Oracle Corporation and/or its
  affiliates. Other names may be trademarks of their respective
  owners.

  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  mysql>
  ```
- Show the available databases
  ```
  mysql> show databases;
  +--------------------+
  | Database           |
  +--------------------+
  | information_schema |
  | items              |
  | mysql              |
  | performance_schema |
  +--------------------+
  4 rows in set (0.00 sec)
  ```
- Use the items database, and create a table in it
  ```
  mysql> use items;
  Database changed
  mysql> CREATE TABLE Projects (id int(11) NOT NULL, name varchar(255) DEFAULT NULL, code varchar(255) default NULL, PRIMARY KEY(id));
  Query OK, 0 rows affected (0.18 sec)

  mysql> show tables
  +-----------------+
  | Tables_in_items |
  +-----------------+
  | Projects        |
  +-----------------+
  1 row in set (0.00 sec)

  mysql>
  ```
- Insert a record into the database, and select it
  ```
  mysql> insert into Projects (id, name, code) values (1, 'DevOps', 'D0180');
  Query OK, 1 row affected (0.00 sec)

  mysql> select * from Projects;
  +----+--------+-------+
  | id | name   | code  |
  +----+--------+-------+
  |  1 | DevOps | D0180 |
  +----+--------+-------+

  mysql>
  ```
