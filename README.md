# Searcher

Tested within expected parameters.
This is a generic searching class for chunks of json or other complex data objects that can accept search queries in a human readable format.
Initialize an instance of the class with a query string (ie, NOT "website" AND ("IP ADDRESS" OR "KEY WORD")), then pass a string or list/tuple/dictionary/complex-mixture-thereof of strings to IsMatch. IsMatch then applies the query to the passed data and returns true if the query is satisfied by the contents of the data. 

Also present in Searcher.py
initialize class with a search query and an option to print self.debug info to console,
then strings or json passed to '__Matched' function will be compared to the query 
and return true/false based on whether it __Matches
search params: AND/OR/NOt, (), "strings", R"regex"
example search parameters:
 "95dd3200bdcd9c9c52a0e2a0b72ce16fd36679a1591a743bb22c50f0bb69bd43"
 "127.0.0.1" AND "ICMP"
 ("blocked" OR "terminated") AND NOT ("by operating system")
 ("blocked" OR "terminated") AND NOT ("by operating system") AND R"Stand(a|A)rd"
 each query or subquery (within parenthesis) must start with a string or regex
 cannot end with NOT
 i.e. "127.0.0.1" AND "ICMP" NOT is not supported
 cannot tolerate AND/OR statements without intervening values
 i.e. "127.0.0.1" AND OR "ICMP" is not supported
 strings to match cannot contain " as these are used to mark the boundaries of the string
 
 To use:
    initialize an instance of the class with the desired query, and optional debug output.
    .IsMatch() accepts a deserialized json object and returns true if the contents 
     of that object match the query criteria.
   .SpecifMatch() also accepts a deserialized json object to check with the set query, however it will check 
   if a specific field in the object meets the query criteria and returns that field if so 
