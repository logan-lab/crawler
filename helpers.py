import json
import re
from collections import defaultdict
from tkinter import *
from nltk.corpus import stopwords


'''For help with tkinter we used https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Add-a-ScrolledText-widget-Tkinter-textarea'''
'''For help with json we used https://docs.python.org/3/library/json.html'''
'''For help with understanding idf we used https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/'''
'''For help with stopwords we used https://pythonspot.com/nltk-stop-words/'''

def tokenize(lines):

    myTok = defaultdict(int)
    words = []
    #iterate through lines in the file
    for line in lines:
        # check pattern, findall combines into list, add to list
        words.extend(re.compile('[a-zA-Z0-9]+').findall(line.lower()))

    # traversing through the list of tokens and adding to dictionary
    for i in words:
        # increment the word count by 1
        myTok[i] += 1

    #returns words and frequencies of the word
    return words, myTok


def createIndex():
    # creates the index
    result = dict()
    pages = 0

    myFile = open('/Users/Logan/PycharmProjects/project3/WEBPAGES_RAW/bookkeeping.json', 'r')
    json_loader = json.load(myFile)  # loads file into variable
    myFile.close()

    for keys in json_loader.keys():  # looks through the final json file
        pages += 1
        x, y = keys.split('/')  # splits keys into x and y based of where the / is

        file = open('/Users/Logan/PycharmProjects/project3/WEBPAGES_RAW' + '/' + x + "/" + y, 'r',
                    encoding='utf-8')  # bs4?
        tokens, freq_dict = tokenize(file)  # tokenizes the file into the variables
        documents = len(tokens)  # gets length of tokenized file

        for word in tokens:
            # counts the frequency of documents, size, uniques
            # if the key is not found in the results
            if word in result:
                pass
            else:
                result[word] = dict()
            if keys not in result[word]:
                # replace the inner dicionary with the word frequency and term frequency
                result[word][keys] = [freq_dict[word], str((freq_dict[word] / documents))]

    return (result, pages)

def searchIndex(index, word):
    #performs the search of the user input through the dictionary that was created
    result = dict()
    if word in index:
        for keys, values in sorted(index[word].items(), key=lambda x: x[1][1], reverse=True):
            result[keys] = values
    return result

def urlResults(index, user_input, json_loader):
    #initialize counter to 0
    ctr = 0
    user_input = user_input.lower()
    #list of searches
    searches = []
    #list of results
    results = []
    #split the user input
    tokens = user_input.split()
    #if the input is only one word
    if (len(tokens) <= 1):
        if user_input not in stopwords.words('english'):
            searches = searchIndex(index, user_input)
    #if user input is more than one word
    else:
        counter = 0
        for word in tokens:
            if word in stopwords.words('english'):
                continue
            #look at the word to see if it is in the urls
            setOfSearches = set(searches)  #create sets
            setOfIndex = set(searchIndex(index, word))  #create sets
            if (counter != 0):
                searches = list(setOfSearches | setOfIndex) #create list
            elif (counter==0):
                searches = searchIndex(index, word)
            counter += 1
    # counts number of urls
    print("URL count for ", user_input, ":", len(searches))
    for i in searches:
        ctr += 1
        #limits the urls to top 20
        if ctr <= 20:
            if i != 'idf':  #makes sure its not the characters "idf"
                results.append(json_loader[i])   #adds to results
    #if the search is not in urls
    if len(results) == 0:
        results.append('Cannot find the specified search')

    #returns the results
    return results


global check
check = 0
def gui(index, json_loader):            #gui function
    window = Tk()                  #gui name
    window.title("CS121 Search Engine")  #creates title of the gui
    window.geometry('1000x600')    #assigns the dimensions of the gui window
    var1 = StringVar()             #creates a variable to receive input from user
    def print():                   #print function to print inside gui
        global check, mylabel
        myResults = ''
        if check > 0:              #checks to see if print has been called already
            mylabel.destroy()      #if it has destroy whatever is printed on gui
        tempResult = urlResults(index, var1.get().lower(), json_loader)
        ctr = 1
        for link in tempResult:
            myResults += str(ctr) + ': ' + str(link) + '\n'  # formats the url and adds it to a string var
            ctr += 1  # increments the counter
        mylabel = Label(window, text=myResults, justify=LEFT)      #creates label for the gui and prints the urls
        mylabel.grid(column=2, row=10)                             #creates the grid for the label
        check += 1
    lbl = Label(window, text="Enter query to search")              #creates the label for the box
    lbl.grid(column=0, row=0)
    txt = Entry(window, width=10, textvariable=var1)               #creates the user input box
    txt.grid(column=0, row=1)
    button = Button(window, text="Search!", command=print)         #creates button
    button.grid(column=1, row=2)
    window.mainloop()                                              #keeps gui up until closed
