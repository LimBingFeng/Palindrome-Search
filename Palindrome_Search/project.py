#import library
import PySimpleGUI as sg
import math
import re
import os.path


# Read in fasta and genbank files
def readFasta(filename):  # read fasta file function
    seq = ''
    fopen = open(filename)  
    lines = fopen.readlines()  

    for line in lines:
        if line.startswith(">"):  # ignore line start with '>'
            pass
        else:  
            line = re.sub('\n', '', line)  # remove \n
            seq += line  # make a string
    return seq.upper() #set return string to uppercase

def readGB(filename):  # read genbank file function
    seq = ''
    seq_gb = '^\s+\d+\s+.+' #regular expression
    fIn = open(filename)
    lines = fIn.readlines()
    
    for line in lines:
        seqline = re.search(seq_gb, line)
        if seqline:
            g1 = seqline.group(0)
            seqline1 = re.sub('[\d\s]', '', g1)
            seq += seqline1 # make a string
    return seq.upper() #set return string to uppercase


# In[3]:


#Find complement, reversed complement and length of sequence
def CnRc(seq):
    complement = {"A": 'T', "C": "G", "G": "C", "T": "A", "_": "_"} #dictionary
    comp = ''.join([complement[base] for base in seq]) #concatenate all complement bases
    rcomp = ''.join([complement[base] for base in seq[::-1]]) #concatenate reversed complement bases
    return comp,rcomp,str(len(seq)) # returning complement, reversed complement and length of sequence

#Check minimum palidrome is odd or even
def isodd(minPalin):
    if (minPalin % 2) == 0:
        return False  # even
    else:
        return True  # odd


#changing list to string
def listToString(seq): 
    temp = "" 
    for i in seq: 
        temp += i+"\n"   
    return temp 
         

#Check for palindrome
def checkPalindrome(seq, minPalin):
    complement = {"A": 'T', "C": "G", "G": "C", "T": "A", "_": "_"}
    l = [] #empty list to store palindromes

    for looptwice in range(0, 2): #looptwice to run odd and even methods
                                  #looptwice = 0 , looptwice = 1
        i = 0 #index position i
        j = 1 #index position j
        
        minPalin += looptwice #1st time: +0
                              #2nd time: +1

        for x in range(len(seq)): # loop through every bases
            
            if isodd(minPalin): # when Odd
                #pass if out of range
                if (i - math.floor(minPalin // 2) < 0 or i + math.floor(minPalin // 2) >= len(seq)):
                    pass
                else:
                    if seq[i] == "_": #odd number palindrome must start with _
                        
                        # quick check whether the last base in range are the same
                        # if no, break 
                        if seq[i - math.floor(minPalin // 2)] == complement[seq[i + math.floor(minPalin // 2)]]:
                            index1 = i
                            index2 = i

                            keepChecking = True
                            #check the bases 2 by 2, extending side way
                            while keepChecking: 
                                if index1 >= 0 and index2 < len(seq): # must be in range
                                    if seq[index1] == complement[seq[index2]]: #if same , extend sideway
                                        index1 -= 1
                                        index2 += 1

                                    elif seq[index1] != complement[seq[index2]]: #not same, stop
                                        temp = seq[index1 + 1:index2] #store the seq from index1 to index2
                                        if len(temp) < minPalin: # if length not fulfil, break 
                                            break
                                        else:
                                            l.append(temp) #if length fulfil, add the string to list l
                                            keepChecking = False #end the loop
                                else: #stop and add to list if out of range
                                    temp = seq[index1 + 1:index2] 
                                    l.append(temp)
                                    keepChecking = False

                        else:
                            pass


            # when Even 
            elif not isodd(minPalin):
                
                #pass if out of range
                if (i - (minPalin // 2) + 1) < 0 or (j + (minPalin // 2) - 1) >= len(seq):
                    pass

                else:
                    if seq[i] == complement[seq[j]]: #if same bases

                        # quick check whether the last base in range are the same
                        # if no, break
                        if seq[i - (minPalin // 2) + 1] == complement[seq[(j + (minPalin // 2) - 1)]]:
                            index1 = i
                            index2 = j

                            keepChecking = True
                            #check the bases 2 by 2, extending side way
                            while keepChecking:
                                if index1 >= 0 and index2 < len(seq): # must be in range
                                    if seq[index1] == complement[seq[index2]]: #if same , extend sideway
                                        index1 -= 1
                                        index2 += 1

                                    elif seq[index1] != complement[seq[index2]]: #not same, stop
                                        temp = seq[index1 + 1:index2] #store the seq from index1 to index2
                                        if len(temp) < minPalin: # if length not fulfil, break 
                                            break
                                        else:
                                            l.append(temp) #if length fulfil, add the string to list l
                                            keepChecking = False  #end the loop
                                else: #stop and add to list if out of range
                                    temp = seq[index1 + 1:index2]
                                    l.append(temp)
                                    keepChecking = False

                        else:
                            pass

            i += 1 #add 1 to index
            j += 1


    palin = listToString(l) #convert list to string (List cannot be used in PysimpleGUI.update )
    return palin

sg.theme("LightGreen") #set theme

# creating three column 
file_list_column = [
    [
        sg.Text("Manual Sequence", size =(17, 1),), sg.InputText() #input manual sequence
    ],
    
    [
        sg.Text("Fasta File"),
        sg.In(size=(56, 1), enable_events=True, key="-FASTA-"), #browse fasta file
        sg.FolderBrowse(),
        
    ],
    [
        sg.Text("GenBank File"),
        sg.In(size=(53, 1), enable_events=True, key="-GENBANK-"), #browse GenBank file
        sg.FolderBrowse(),
    ],
    
     [
        sg.Text("Min Palindrome Length", size =(17, 1),), sg.InputText() #input palindrome length
    ],
    
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 30), key="-FILE LIST-" #create a box
        )
    ],
    
    [
        sg.Text("Click on one file to run") #create run button
    ],
    
    [
        sg.Button("Run"),sg.Button("Cancel") #create cancel button
    ]
]

output_column = [
    [sg.Text(size=(50, 40), key="-OUT-")], # 2nd column with output seq, comp, rcomp and length
]

palindrome_column = [
    [sg.Text(size=(50, 40), key="-PALIN-")], # 3rd column with palindrome output
]

layout = [                               #combining every thing 
    [
        sg.Column(file_list_column),
        sg.VSeperator(), #create separator
        sg.Column(output_column),
        sg.VSeperator(), #create separator
        sg.Column(palindrome_column)
    ]
]

window = sg.Window("Group Project", layout) #combining everything and make a window

while True:
    event, values = window.read()
    
    if event == "Cancel" or event == sg.WIN_CLOSED: #if event = cancel or close, break
        break
    
    if event == "Run": #if run button clicked
        seq = values[0] #get the input sequence
        minPalin = int(values[1]) #get the input min palin length
        seq = seq.upper() #set to uppercase
        comp,rcomp,length = CnRc(seq) 
        palin = checkPalindrome(seq, minPalin)
                
        #printing everything 
        window["-OUT-"].update("Fasta Sequence: " + seq +
                               "\n\nComplement: " + comp +
                               "\n\nReversed Complement: " + rcomp +
                               "\n\nNumber of Base Pair: " + length)
                
        window["-PALIN-"].update("Palindromes: \n" + palin )
    
    #Searching for fasta file 
    if event == "-FASTA-":
        folder = values["-FASTA-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.endswith((".fasta"))
        ]
        window["-FILE LIST-"].update(fnames) #list out all the fasta file
        
    #Searching for genbank file     
    if event == "-GENBANK-":
        folder = values["-GENBANK-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".gb"))
        ]
        window["-FILE LIST-"].update(fnames) #list out all the genbank files
    
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FILE LIST-"][0]
            )
            if filename.endswith(".fasta"):
                seq = readFasta(filename) #get the input sequence
                minPalin = int(values[1]) #get the input min palin length
                comp,rcomp,length = CnRc(seq)
                palin = checkPalindrome(seq, minPalin)
                
                #printing everything
                window["-OUT-"].update("Fasta Sequence: " + seq +
                                       "\n\nComplement: " + comp +
                                       "\n\nReversed Complement: " + rcomp +
                                       "\n\nNumber of Base Pair: " + length)
                
                window["-PALIN-"].update("Palindromes: \n" + palin )
                
            elif filename.endswith(".gb"):
                seq = readGB(filename) #get the input sequence
                minPalin = int(values[1]) #get the input min palin length
                comp,rcomp,length = CnRc(seq)
                palin = checkPalindrome(seq, minPalin)
                
                #printing everything
                window["-OUT-"].update("GenBank Sequence: " + seq +
                                       "\n\nComplement: " + comp +
                                       "\n\nReversed Complement: " + rcomp +
                                       "\n\nNumber of Base Pair: " + length)
                
                window["-PALIN-"].update("Palindromes: \n" + palin )
                

        except:
            pass
window.close()

