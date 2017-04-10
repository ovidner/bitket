Bitket
======
A ticket platform for Linköping University, formerly named Tickle. It has been 
used in the wild in different shapes at the following events:
* SOF 2015
* LiTHe Blås Luciafest 2015
* LiTHe Blås Luciafest 2016

## Functional specification
Bitket is a fairly advanced application, with features including
* flexible discount management, e.g. for union discounts
* login management using Google, Facebook and LiU SSO (ADFS/OAuth2)
* purchasing queue that gracefully handles massive, concurrent load without 
  overshooting the maximum allowed ticket count
* support for variations of ticket types (even with different pricing), e.g. for
  letting visitors choose beverage at a *sittning*
* secure payments with credit/debit card through Stripe
* pre-purchase access using unique links, allowing purchase of a defined number 
  of tickets before public release
* entry handling, using visitor's LiU cards or QR codes

## Technological specification
Bitket is roughly divided into a backend and a frontend. Both are completely 
separate applications, giving the potential advantages of independent scaling or 
sharding.

The backend is a Django application with PostgreSQL as a data store, exposing a 
REST API. It features integrations to services including (but not limited to) 
* Facebook (OAuth2)
* Google (OAuth2)
* LiU ADFS (OAuth2)
* Sesam (LiU integration platform)
* Stripe
* Kobra

Directly visible to the user, the frontend fetches data, partly from the Bitket 
API, partly from services such as
* Facebook (OAuth2)
* Google (OAuth2)
* LiU ADFS (OAuth2)
* Stripe

This data is then sent to the backend and/or presented in a meaningful way, 
using mainly React and Redux. It is rebuilt on every code change (or deployment) 
through `react-scripts` (i.e. Babel+Webpack).

Deployment is handled with Docker, including Compose. Docker builds are 
performed by Gitlab CI.

## Scope for the TDDD27 course
[1] Implementing fully managed reselling of tickets, meaning that Bitket takes 
all the risk of reselling a ticket (also reducing the vector for inordinate 
prices). This is done by charging the new ticket owner for the ticket while 
simultaneously refunding the previous owner's part and transferring the actual 
ticket ownership. This is already partly implemented.

[2] Implementing an asynchronous queue+worker architecture for handling ticket 
purchases, replacing the existing synchronous flow. This will be realized using 
Celery as the asynchronous queue/broker and Django Channels as the messaging 
solution (notifying the client that the purchasing process has been carried 
out, using Websockets/HTTP2).
