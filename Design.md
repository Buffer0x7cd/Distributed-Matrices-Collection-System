# Design of a distributed matrice collection System.    
## Considerations: Pull vs Push Model

During design of a monitoring system we can use two different type of monitoring system.    
### Push Based   
In a push based monitoring system metrices are pushed to a remote server based on occurence of events, these events can be a threshold or a simple cron job.    
### Pros    
In a push based model there is no need of a service discvory mechanism. each node can have the access to it's assigned matrices server which it can push the matrices too.

The Server doesn't need to poll a list of nodes that it need to monitor to, in order to check for new matrices

This type of system can easily work on devices that are not publiclly exposed but have a limited internet connectvity.

### Cons
In a push based model, checking for availiability of a node becomes harder, due to fact that the server don't have a list of nodes that are supposed to send the matrices, so in case if a node is down, there is no way for server to know it's status

In push based model, the type and amount of matrice sent are controlled by client, that makes it harder to change the type or amount of matrices sent by server.( we can overcome this by allowing a bi-directional communication channle which can be used to alter the config of clients from server so that, the matrices can be changed, but this involves adding an extra layer of functionality)

## Pull based Model

In a pull based monitoring system, each client will have a agent running on it's system, this agent will collect the system matrices and expose an endpoint at that node which can be used by the server to access the matrices of this host. example Prometheus

## Pros    
In this type of system health check of nodes becomes easy due to the fact that , the server already have the list of nodes, which can be used to check the status of each node

Controlling the type and amount of matrices becomes easy due to the fact that, the server is responsible for scraping the data from each node.

## Cons
The Pull mechanism is based on polling, which can increase the network load

The Nodes are needed to exposed to public net

It adds a security consideration by opening a port on which all system matrices are available, so proper methdos of authentication and authorization are needed to make sure that only the monitoring server have access to this type of data. 

## Our Desired Goal For the system ##    
1. It should work on networks that are behind NAT.
2. It should require minimum internet connectvity


Based on above two factors A push based solution is ideal for our Use case.

## Tech Stack   
**1. Riemann Agents:**  Riemann is a matrice collecction system which can push local matrices to a remote riemann server based on event. in our case these events are periodic time. on each server the local Riemann server will collect the matrice for a set period of time. after that period of time is over, it will push the collected matrices to the remote riemann server and discard the local collection.
All riemann nodes are shredded based on therir geographic location.

**2. Riemann Server:** Riemann server will act as a listner and listem for the data that is emitted from differnt Riemann clients. Each server will have a temporary cache. the server will use this cache to store the incoming data before flushing them to a persistant storage.

**3. InfluxDB Cluster:**: Influx DB is a Time Series Database. We will use influx DB to store the matrices that are being flushed from differnet Riemann Server. This will provide us a centalt storage for Matrices which can be later used in visulization.

**4. Grafana:** A grafana instance will be connected with the InfluxDB, we will use grafana for visulization of the time series data that is stored in the InfluxDB Cluster.

![Diagram](https://github.com/Buffer0x7cd/Distributed-Matrices-Collection-System/raw/master/matrices.png)