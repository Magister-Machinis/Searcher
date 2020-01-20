# Searcher

STILL VERY WIP, needs a boat-load of testing still


This is a generic searching class for chunks of json or other complex data objects that can accept search queries in a human readable format.
Initialize an instance of the class with a query string (ie, NOT "website" AND ("IP ADDRESS" OR "KEY WORD")), then pass a string or list/tuple/dictionary/complex-mixture-thereof of strings to IsMatch. IsMatch then applies the query to the passed data and returns true if the query is satisfied by the contents of the data. 
Obviously there is quite a bit more documentation to do, and I would like regex support as well (and all the testing needed to make sure it runs right). Stay tuned for more info.
