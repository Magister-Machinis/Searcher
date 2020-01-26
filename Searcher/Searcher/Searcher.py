
#initialize class with a search query and an option to print debug info to console,
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
        while count < len(inputstring):
            if inputstring[count:count+3] == "AND":                
                self.parsedsearch.append(1)
                count+=3
            elif inputstring[count:count+2] == "OR":                
                self.parsedsearch.append(2)
                count+=2
            elif inputstring[count:count+3] == "NOT":
                self.parsedsearch.append(3)
                count+=3
            elif inputstring[count]=='"':
                count+=1
                temp = []
                flag = True
                while flag == True:
                    if inputstring[count] == '"':                        
                        self.parsedsearch.append(''.join(map(str,temp)).lower())
                        flag = False
                    else:
                        temp.append(inputstring[count])
                    count+=1
            elif inputstring[count] == '(':                
                count+=1
                temp = []
                flag = True
                while flag == True:
                    if inputstring[count] == ')':                        
                        self.parsedsearch.append(Searcher(''.join(map(str,temp))))
                        flag = False
                    else:
                        temp.append(inputstring[count])
                    count+=1
            else:
                count+=1
    
    def IsMatch(self, data):
        self.data=data
        truth,count=self.__Match()
        self.data=None
        return truth

    #iterates through the saved search arranges the string comparisons between assorted ANDs and ORs,
    #inverting where a NOT indicates to do such or dropping into a subsearch where () had indicated, 
    #then initiates the __checking function when a string is iterated over to initiate a search of the data passed in
    def __Match(self, count=0, truth=None):
        
        nottest =True
        while (count < len(self.parsedsearch)):
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
                    if(nottest==False):
                        temp1,temp = self.parsedsearch[count].__Match()
                        truth = not temp1
                    else:
                        truth,temp = self.parsedsearch[count].__Match()                    
                    count+=1   
       

        return bool(truth), int(count)

#now that a string to compare has been identified, this iterates through the data to determine if it is present or not
    def __check(self,count,data =None):
        checker = False
        if data ==None:
                data= self.data
            
        if isinstance(data, list) or isinstance (data,tuple):
            while len(data)>0:
                if(self.__check(count, data.pop(0))):
                    checker=True
        elif isinstance(data,dict):
            for key in list(data.keys()):
                if(self.__check(count,data.pop(key))):
                    checker = True
        else:
            if self.parsedsearch[count] in data:
                checker = True
        return checker