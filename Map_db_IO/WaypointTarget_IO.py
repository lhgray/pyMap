#
# Module of input and output functions for geographic waypoints
#
#   Currently in development and used for testing
#
import math
site_utm_db={}    # initialize the Site database as a dictionary
input_db={}
temp_db={}

#===============================================================================
#   Function 'InputUTMSites'
#

def InputUTMSites(    # does not allow duplicate SiteIDs
    inputfilename   # string, text file of UTM coordinates
    ):
    '''
    Probably deprecated. This needs to be checked
    '''
# TODO: Check that this function is not required or called !
    
    wpinput=open(inputfilename, 'r')
    global site_utm_db    
    while 1:
        wpline=wpinput.readline()   # read one line
        if not wpline:break         # continue if the line was not blank(EOF)
        wpline=wpline.strip()       # remove whitespace
        wpline=wpline.strip('\n\t') # remove tabs and returns
        item=wpline.split(',')      # split the line using commas as delimiters
        # checks that the first field of item is not blank then create a new item in targe_db
        # using the waypoint ID, the first field in item, as the key
        # otherwise append the item fields to the current values using the last key value
        if item[0] != '':          
            site_utm_db[item[0]]=[(int(item[1]),
                                     int(item[2]),
                                     int(item[3]),
                                     item[4].strip(),
                                     item[5].strip()
                                     )]
            lastkeyused=item[0] # remember the last key value if required
        else:   # append the current data to the last set
            site_utm_db[lastkeyused].append(
                (int(item[1]),
                int(item[2]),
                int(item[3]),
                item[4].strip(),
                item[5].strip())
                )
    wpinput.close()

#==========================================================================================
#   The function 'newInputUTMSites' assumes that each line has the SiteID field explicitly
#

def newInputUTMSites( # allows duplicate SiteID's
    inputfilename   # string, text file of UTM coordinates
    ):
    '''
    Probably deprecated. This needs to be checked
    '''
# TODO: Check that this function is not required or called !
    
    wpinput=open(inputfilename, 'r')
    global site_utm_db    
    while 1:
        wpline=wpinput.readline()   # read one line
        if not wpline:break         # continue if the line was not blank(EOF)
        wpline=wpline.strip()       # remove whitespace
        wpline=wpline.strip('\n\t') # remove tabs and returns
        item=wpline.split(',')      # split the line using commas as delimiters
        #
        # using the SiteID, the first field in item, as a dictionary key
        # check that it is not a duplicate of an existing key in Site_db
        # if it is, append the item fields to the current values using the last key value
        # otherwise, create a new dictionary entry
        #
        if site_utm_db.has_key(item[0]):   # append the current data to the last set
            site_utm_db[item[0]].append(
                (int(item[1]),
                int(item[2]),
                int(item[3]),
                item[4].strip(),
                item[5].strip())
                )         
        else:   # create a new dictionary entry
            site_utm_db[item[0]]=[(int(item[1]),
                                     int(item[2]),
                                     int(item[3]),
                                     item[4].strip(),
                                     item[5].strip()
                                     )]
 
    wpinput.close()

#=======================================================================================
# function 'ReadDatabase'


def ReadDatabase(
    inputfilename
    ):
    '''
    A function to read a generic text database in which the fields are delimited by commas.
    Each new record is indicated by a new line.
    
    A record in which the first field is 'Captions' provides descriptions of the fields
    in each record. The second field is a database type, 'site', 'plan', 'cfg'...
    and others not yet specified. The 3rd field and beyond are field titles used for
    presentation in GUI interfaces. The 2nd field is used to select functions for
    processing.
    
    The data is placed into a dictionary named 'input_db' in which the first field of each
    record is used as the key. Subsequent data fields are stored as strings in a tuple.
    
    Any record in which the first field is identical to a key already in use, will have its
    subsequent data fields placed in another tuple in a list of tuples associated with the same
    dictionary key
    
    ie. input_db = {key: [(...),(...),---,(...)], key2: [(...)], key3: etc...}
    
    All data is stored as strings. Other functions are used to convert strings
    to integers, floats or whatever.
    '''
    input_db = {}
    wpinput=open(inputfilename, 'r')

    while 1:
        wpline=wpinput.readline()   # read one line
        if not wpline:break         # continue if the line was not blank(EOF)
        wpline=wpline.strip()       # remove whitespace
        wpline=wpline.strip('\n\t') # remove tabs and returns
        item=wpline.split(',')      # split the line using commas as delimiters
        #
        # the first field in item is used as a dictionary key
        # check that it is not a duplicate of an existing key in input_db
        # if it is, append the item fields to the current values using the last key value
        # otherwise, create a new dictionary entry
        #
        item2add=tuple(item[1:len(item)]) # create a new item and ensure its a tuple
        #
        if input_db.has_key(item[0]):   # if the key exists in input_db 
             input_db[item[0]].append(item2add) # append the current data to the key's value
        else:
            input_db[item[0]]=[]    # create a new key
            input_db[item[0]].append(item2add)  #append the data to the new key's null value
    wpinput.close()
    return(input_db)

#=====================================================================================
#   Function 'generic2site'
#

def generic2site_db(
    input    # dict, the name of a dictionary
    ):
    '''
    A function to reformat a generic dictionary based database that was created from a
    site waypoint database file. The function primarily converts strings to integers or floats
    as required and converts values into the default units to be used in 'FlightDirector'
    
    There are no checks to ensure that the database passed is a site Waypoint Database
    '''     
    for key in input.keys():
        if key.title() == 'Captions':   # ignore the 'Captions' record
            continue
        for x in range(len(input[key])):
            input[key][x] = list(input[key][x])       # convert the tuple to a list
            input[key][x][0] = int(input[key][x][0])  # convert the zone string to int
            for y in (1,2):
                try:
                    input[key][x][y] = int(input[key][x][y]) # return all but the last character
                except ValueError:
                    input[key][x][y] = float(input[key][x][y])
                    input[key][x][y] = int(input[key][x][y])                
##            input[key][x][1] = int(input[key][x][1])  # convert the northing string to int
##            input[key][x][2] = int(input[key][x][2])  # convert the easting string to int
            input[key][x][3] = input[key][x][3].strip()   # removes leading/trailing whitespace
            for y in (4,5,6,7):
                if input[key][x][y][-1].isalpha():      # is the last character alpha?
                    if input[key][x][y][-1].lower()=='f':
                        try:
                            input[key][x][y] = int(input[key][x][y][:-1]) # return all but the last character
                        except ValueError:
                            input[key][x][y] = float(input[key][x][y][:-1])
                        input[key][x][y] = int(input[key][x][y]/3.2808399)   # feet to metres and truncate to an int
                    else:
                        try:
                            input[key][x][y] = int(input[key][x][y][:-1])
                        except ValueError:
                            input[key][x][y] = float(input[key][x][y][:-1])
                else:
                    try:
                        input[key][x][y] = int(input[key][x][y])
                    except ValueError:
                        input[key][x][y] = float(input[key][x][y])
                        
            input[key][x][8] = input[key][x][8].strip()
            input[key][x] = tuple(input[key][x])      # convert the list to a tuple
 
    site_utm_db = {}
    site_utm_db = input # just for test
    return(site_utm_db)

#=====================================================================================
#   Function 'generic2planning_db'
#
def generic2plan_db(input):
    '''
    A function to reformat a generic dictionary database created from a planning
    database file. The function primarily converts strings to integers or floats
    as required and converts values into the default units to be used in
    'FlightDirector'
    '''

    dig_sign=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', '+']
    for key in input.keys():
        if key.title() == 'Captions':   # ignore the 'Captions' record
            continue
        for x in range(len(input[key])):
            input[key][x]=list(input[key][x])       # convert the tuple to a list
            for y in range(len(input[key][x])):
                input[key][x][y]=input[key][x][y].strip()   # removes leading/trailing whitespace
                # is the last and only the last character alpha? Otherwise ignore
                #if (input[key][x][y][0].isdigit() and input[key][x][y][-1].isalpha()):
                if input[key][x][y][0] in dig_sign:
                    if input[key][x][y][-1].isalpha():
                        if input[key][x][y][-1].lower()=='f':
                            # convert feet to metres
                           input[key][x][y]=float(input[key][x][y][:-1]) # return all but the last character
                            # feet to metres and round to an int
                           input[key][x][y]=round((input[key][x][y]/3.2808399),0)
                        elif input[key][x][y][-1].lower()=='k':
                            # convert 'knots' to metres/sec
                            input[key][x][y]=float(input[key][x][y][:-1])
                            input[key][x][y]=round((input[key][x][y]*1852/3600),1)    
                        elif input[key][x][y][-1].lower()=='m':
                            input[key][x][y]=float(input[key][x][y][:-1])
                            input[key][x][y]=round(input[key][x][y],1)
                        else:
                            print 'Unknown character terminating numerical string'
                    else:
                        try:
                            input[key][x][y]=int(input[key][x][y])
                            # integer values are normally expected, but if the 
                            # user has input a float value, this will work
                        except ValueError:
                            input[key][x][y]=float(input[key][x][y])
                else:
                    continue
                
            # aggregate the view angles into a single object
            #
            temp = []
            temp = [input[key][x][8+z] for z in range(int(input[key][x][7]))]
            temp = tuple(temp)
            input[key][x][8] = temp # replace the first view angle with the list
            for z in range(1,int(input[key][x][7])):
                input[key][x].pop(9)   # remove the extraneous view angles
                    
            input[key][x]=tuple(input[key][x])      # convert the list back to a tuple

    plan_utm_db = {}
    plan_utm_db = input
    return(plan_utm_db)

#====================================================================
#   Function 'generic2sensor_db'
#

def generic2sensor_db(
    input    # dict, the name of a dictionary
    ):
    '''
    A function to reformat a generic dictionary database created from a sensor configuration
    database file. The function primarily converts strings to integers or floats
    as required and converts values into the default units to be used in 'FlightDirector'    
    ''' 
       
    for key in input.keys():
        if key.title() == 'Captions':   # ignore the 'Captions' record
            continue
        input[key][0] = list(input[key][0])             # convert the tuple to a list
        input[key][0][0] = input[key][0][0].strip()     # strip the sensorID
        input[key][0][1] = input[key][0][1].strip()     # strip the mode type
        for x in range(2, 7, 1):                        # convert the next 5 fields to integers
            input[key][0][x] = int(input[key][0][x])
        for x in range(7, len(input[key][0]), 1):       # convert the remaining fields to floats
            input[key][0][x] = float(input[key][0][x])
        input[key][0] = tuple(input[key][0])               # convert the list to a tuple

    sensor_db = {}
    sensor_db = input
    return(sensor_db)

#===============================================================================
#   test stuff
#

if __name__ == "__main__":

    #======================================
    #test the input of a site database file
    
    mytestfile=r'C:\Documents and Settings\Owner\My Documents\Python\pyMap\test_1_sites.txt'

    temp_db = ReadDatabase(mytestfile)

    print temp_db,'\n'
    site_utm_db = generic2site_db(temp_db) # the site database
    print site_utm_db,'\n'
    
    for key in site_utm_db.keys():
        if key == 'Captions': continue  # ignore the Captions
        for x in range(len(site_utm_db[key])):
            print 'Site',key, 'Pt#',x, site_utm_db[key][x]

    #======================================
    #test the input of a planning database file  
                    
    mytestfile=r'C:\Documents and Settings\Owner\My Documents\Python\pyMap\test_1_plan.txt'

    temp_db = ReadDatabase(mytestfile)

    print temp_db,'\n'    
    plan_utm_db = generic2plan_db(temp_db)   # the planning database    
    print plan_utm_db,'\n'
    
    for key in plan_utm_db.keys():
        if key == 'Captions': continue  # ignore the Captions
        for x in range(len(plan_utm_db[key])):
            print 'Site',key, 'Pt#',x, plan_utm_db[key][x]

    #======================================
    #test the input of a sensor configuration database file  
                    
    mytestfile=r'C:\Documents and Settings\Owner\My Documents\Python\pyMap\casi302_config.txt'

    temp_db = ReadDatabase(mytestfile)
    print temp_db,'\n'    
    sensor_db = generic2sensor_db(temp_db)   # the sensor database
    
    print sensor_db,'\n'
    
    for key in sensor_db.keys():
        if key == 'Captions': continue  # ignore the Captions
        print 'Configuration', key, sensor_db[key]
