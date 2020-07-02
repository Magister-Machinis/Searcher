import re
import json

#initialize class with a search query and an option to print self.debug info to console,
#then strings or json passed to '__Matched' function will be compared to the query 
#and return true/false based on whether it __Matches
#search params: AND/OR/NOt, (), "strings", R"regex"
#example search parameters:
# "95dd3200bdcd9c9c52a0e2a0b72ce16fd36679a1591a743bb22c50f0bb69bd43"
# "127.0.0.1" AND "ICMP"
# ("blocked" OR "terminated") AND NOT ("by operating system")
# ("blocked" OR "terminated") AND NOT ("by operating system") AND R"Stand(a|A)rd"
# each query or subquery (within parenthesis) must start with a string or regex
# cannot end with NOT
# i.e. "127.0.0.1" AND "ICMP" NOT is not supported
# cannot tolerate AND/OR statements without intervening values
# i.e. "127.0.0.1" AND OR "ICMP" is not supported
# strings to match cannot contain " as these are used to mark the boundaries of the string
# 
# To use:
#    initialize an instance of the class with the desired query, and optional debug output.
#    .IsMatch() accepts a deserialized json object and returns true if the contents 
#     of that object match the query criteria.
#   .SpecifMatch() also accepts a deserialized json object to check with the set query, however it will check 
#   if a specific field in the object meets the query criteria and returns that field if so 



class searcher(object):    

    def __init__(self, inputstring,debug=False):
        self.parsedsearch=[]
        self.debug=debug
        count = 0
        
        if self.debug:
            print(f"processing {inputstring}")

        while count < len(inputstring):
            if self.debug:
                print(inputstring[count])
            if inputstring[count:count+3] == "AND":                
                self.parsedsearch.append(1)
                count+=3
                if self.debug:
                    print(f"processing AND")
            elif inputstring[count:count+2] == "OR":                
                self.parsedsearch.append(2)
                count+=2
                if self.debug:
                    print(f"processing OR")
            elif inputstring[count:count+3] == "NOT":
                self.parsedsearch.append(3)
                count+=3
                if self.debug:
                    print(f"processing NOT")
            elif inputstring[count]=='R' and inputstring[count+1] =='"':
                count+=2
                temp = []
                flag = True
                while flag == True:
                    if inputstring[count] == '"':                        
                        self.parsedsearch.append(re.compile(''.join(map(str,temp))))
                        flag = False
                    else:
                        temp.append(inputstring[count])
                    count+=1
                if self.debug:
                    print(f"processing regex of {temp}")
            elif inputstring[count]=='"':
                count+=1
                temp = []
                flag = True
                while flag == True:
                    if inputstring[count] == '"':                        
                        self.parsedsearch.append(''.join(map(str,temp)))
                        flag = False
                    else:
                        temp.append(inputstring[count])
                    count+=1
                if self.debug:
                    print(f"processing string of {temp}")
            elif inputstring[count] == '(':                
                count+=1
                temp = []
                flag = True
                while flag == True:
                    if inputstring[count] == ')':                        
                        self.parsedsearch.append(searcher(''.join(map(str,temp))))
                        flag = False
                    else:
                        temp.append(inputstring[count])
                    count+=1
                if self.debug:
                    print(f"processing subsearch with {temp}")
            else:
                count+=1
        if self.debug:
            print(f"query processed as {self.parsedsearch}")
    
    #wrapper for general match protocol
    def IsMatch(self, data,subdata=0):        
        self.data=[data]        
        if self.debug:
            print(f"Checking query against {data}")        
        truth,count=self.__Match(subdata=subdata)
        self.data=None
        if self.debug:
            print(f"final truth is {truth}")
        return truth
    
    #iterates through the saved search arranges the string comparisons between assorted ANDs and ORs,
    #inverting where a NOT indicates to do such or dropping into a subsearch where () had indicated, 
    #then initiates the __checking function when a string is iterated over to initiate a search of the data passed in    
    def __Match(self, count=0, truth=None,subdata=None):
        if self.debug:
            print(f"current truth is {truth}")
        nottest =True
        while (count < len(self.parsedsearch)):
            if self.debug:
                print(f"current truth is {truth}")
    
            #determines whether we are inverting the results of this part
            if(self.parsedsearch[count] == 3):
                    nottest = False
                    count+=1

            if(self.parsedsearch[count] == 1):
                    temp,count = self.__Match(count=count+1,truth=truth,subdata=subdata)
                    if(truth == None):
                        truth=temp
                    else:
                        truth = truth and temp

            elif(self.parsedsearch[count] == 2):
                    temp,count = self.__Match(count=count+1,truth=truth,subdata=subdata)
                    if(truth == None):
                        truth=temp
                    else:
                        truth = truth or temp
        
            elif(isinstance(self.parsedsearch[count],str)):
                    truth = self.__check(count=count,subdata=subdata) and nottest
                    count+=1
            elif(isinstance(self.parsedsearch[count],re.Pattern)):
                    truth = self.__check(count=count,subdata=subdata) and nottest
                    count+=1
            elif("searcher" in str((self.parsedsearch[count]))):
                    truth =  self.parsedsearch[count].IsMatch(self.data,subdata=subdata) and nottest     
                    count+=1   
       
        if self.debug:
            print(f"returning truth as {truth}")
        return bool(truth), int(count)

    #now that a string to compare has been identified, this iterates through the data to determine if it is present or not
    def __check(self,count,data =None,subdata=0):
        
        checker = False
        if subdata !=None:
                data= subdata
        elif data == None:
            data=self.data
        if self.debug:
            print(f"checking {self.parsedsearch[count]} against {data}")    
        if isinstance(data, list) or isinstance (data,tuple):
            for item in data:
                if(self.__check(count, item)):
                    checker=True
        elif isinstance(data,dict):
            for key in data.keys():
                if(self.__check(count,data[key])):
                    checker = True
        else:
            if self.debug:
                print(f"found {data}")
                            
            if isinstance(self.parsedsearch[count],re.Pattern):
                if self.parsedsearch[count].search(str(data)):
                    if self.debug:
                        print("Match!")
                    checker = True
            else:
                if self.parsedsearch[count] in str(data):
                    if self.debug:
                        print("Match!")
                    checker = True
        return checker

    #ensures that results are cleared from object
    def _innerSpecificMatch(self,data):
        if isinstance(data, list):
            self.data=data    
        else:
            self.data=[data]
         
        if self.debug:
            print(f"Checking query against {data}")                
        try:
            for item in self._SMatch(self.data):
                yield item
        except Exception as e:
            raise e
        finally:
            self.data=None

    #sends data to the _Match() function to see if it fits, then yields up if it does
    def _SChecker(self,data,count=0):
        self.data.append(data)
        if self.debug:
            print(f"Checking if {data} is a match")
            print(f'data set is {self.data}')
            print(f'{len(self.data)}')
        truth,count=self.__Match(subdata=self.data[-1])
        del self.data[-1]
        if truth:
            if self.debug:
                print("Matched!")
            yield data

    #general loop to iterate through object down to leaf items
    def _SMatch(self, data):               
        if self.debug:
            print(f'reviewing {data}')
            print(type(data))
        if isinstance(data, list) or isinstance(data, tuple):            
            for item in data:
                for subitem in self._SMatch(item):
                    yield subitem
        elif isinstance(data, dict):            
            print(list(data))
            for key in list(data):
                for item in self._SMatch(data[key]):
                    yield item          
        else:
            for item in self._SChecker(str(data)):
                yield item

    #user presenting wrapper to specific match option
    def SpecificMatch(self, data):  
         data = [test for test in (item for item in self._innerSpecificMatch(data))]
         if self.debug:
            print(f"results are {data}")
         return data