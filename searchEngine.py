import os
import json
import math
import helpers



if __name__ == '__main__':
    index = None
    documents = None
    uniqueWords = None

    if os.path.isfile('Results.json'):                  #checks to see if json file exists
        print('Reading from Results.json')
        file1 = open('Results.json', 'r')
        index = json.load(file1)
        file1.close()
        uniqueWords = len(index)                        #gets number of uniqueWords

    else:
        print('Creating index for Results.json')
        index, documents = helpers.createIndex()
        uniqueWords = len(index)                        #gets number of uniqueWords

        for keys in index.keys():                       #iterates through keys in dict
            idf = 0
            if len(index[keys]) != 0:                   #length cant be 0 due to the divide below
                idf += math.log(documents / len(index[keys])) #how to calculate idf
            index[keys]['idf'] = str(idf)          #inputs it into index

        file3 = open('Results.json', 'w')
        json.dump(index, file3)
        file3.close()

        size = os.path.getsize("Results.json")
        file5 = open('Results.txt', 'w')
        file5.write('Number of documents: ' + str(documents) + '\n')
        file5.write('Number of uniques: ' + str(uniqueWords) + '\n')
        file5.write('Size of index on file: ' + str(size/1000) + ' kbytes')
        file5.close()

    myFile = open('/Users/Logan/PycharmProjects/project3/WEBPAGES_RAW/bookkeeping.json', 'r')
    json_loader = json.load(myFile)
    myFile.close()

    helpers.gui(index, json_loader) #opens gui
