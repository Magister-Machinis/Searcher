
#initialize class with a search query and an option to print self.debug info to console,
#then strings or json passed to '__Matched' function will be compared to the query 
#and return true/false based on whether it __Matches
#search params: AND/OR/NOt, (), "strings"
#example search parameters:
# "127.0.0.1" AND "ICMP"
# ("blocked" OR "terminated") AND NOT ("by operating system")
# "95dd3200bdcd9c9c52a0e2a0b72ce16fd36679a1591a743bb22c50f0bb69bd43"
# must start with a string
# cannot end with NOT
# cannot tolerate AND/OR statements without intervening values
# will add regex laters

class searcher(object):    

    
    def __init__(self, inputstring,debug=False):
        self.parsedsearch=[]
        self.debug=debug
        count = 0
        
        if self.debug:
            print(f"processing {inputstring}")

        while count < len(inputstring):

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
    
    def IsMatch(self, data):
        self.data=data
        if self.debug:
            print(f"Checking query against {data}")
        truth,count=self.__Match()
        self.data=None
        if self.debug:
            print(f"final truth is {truth}")
        return truth

    #iterates through the saved search arranges the string comparisons between assorted ANDs and ORs,
    #inverting where a NOT indicates to do such or dropping into a subsearch where () had indicated, 
    #then initiates the __checking function when a string is iterated over to initiate a search of the data passed in
    def __Match(self, count=0, truth=None):
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
                    temp,count = self.__Match(count+1,truth)
                    if(truth == None):
                        truth=temp
                    else:
                        truth = truth and temp

            elif(self.parsedsearch[count] == 2):
                    temp,count = self.__Match(count+1,truth)
                    if(truth == None):
                        truth=temp
                    else:
                        truth = truth or temp
        
            elif(isinstance(self.parsedsearch[count],str)):
                    if(nottest==False):
                        truth = not(self.__check(count))
                    else:
                        truth = self.__check(count)
                    count+=1
            elif("searcher" in str((self.parsedsearch[count]))):
                    truth =  self.parsedsearch[count].IsMatch(self.data) and nottest     
                    count+=1   
       
        if self.debug:
            print(f"returning truth as {truth}")
        return bool(truth), int(count)

#now that a string to compare has been identified, this iterates through the data to determine if it is present or not
    def __check(self,count,data =None):
        if self.debug:
            print(f"checking {self.parsedsearch[count]} against {data}")
        checker = False
        if data ==None:
                data= self.data
            
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
            if self.parsedsearch[count] in str(data):
                if self.debug:
                    print(f"Match!")
                checker = True
        return checker