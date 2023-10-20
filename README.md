# ApiTesting

This automatic testing framework is implemented on the API provided by the Lufthansa company.   
It contains 2 main folders: 
1. A package called **request_api** which will contain all the API requests mapped according to the documentation in the form of methods
2. A package called **tests** that will contain all the tests we do by calling the previous methods     

The first document uses the REQUESTS library with which the requests are executed, and the second one uses the unittest library.
This API provides us with a wealth of information, such as flight schedules and lists of airports, airlines, aircraft, countries and cities.