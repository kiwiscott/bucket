![Alt text](/doc/bucket.png)


## Bucket

> This project serves two purposes. The first is to server as a bucket  for some of our projects to store documents in cassandra. The second is a learning project with different python technologies.


## architecture

Code design wide this project implements full end to end coverage:
+ written as test first
+ an architecture build on inward facing dependencies only. This is an interesting view on how to develop software and very much aligned to my own. Everything is testable from the start and technology decision are deffered. v1 of the application is the entities, use case code only. (https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)


![Alt text](/doc/arch.png)

Using this architecture approach is different from using django where the framework drives the strcuture of the code. In this case the core application depends on no frameworks. Adding the rest api components is acase of choosing a light weight web framework that solves only that problem. Additionally designed the cassandra gateway is purly based on the recommended structure of cassandra - a nosql datastore without joins. 


## code
![Alt text](/doc/tenant-bucket-item.png)

The domain is fairly simple. Tenants are assigned access key. They use these access keys to create buckets. Once the tenant has a bucket they can start adding and removing items from the buckets. The items in the buckets are designed to be a stream of bytes.