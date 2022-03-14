#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# GuangSin_Lu, 2022-Ｍar-5, Modify TODO part and my own code
# GuangSin_Lu, 2022-Ｍar-6, Workign script, editing docstrings 
# GuangSin_Lu, 2022-Ｍar-13, Adding exception handling and store data in binary
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
strID =None # User ID input
strTitle = None # User Title input
strArtist= None # User Artist input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row'
strFileName = 'CDInventory.dat' # data storage file
objFile = None  # file object



# -- PROCESSING -- #
#Definition of Classes and functions:

class DataProcessor:
    #  Add functions for processing CD data
    """Processing the data from user selection, add delete or save"""
    
    @staticmethod
    def add_inventory(table):
        """Function to add CD inventory from user input.
        Gets user input from userinput() function in the IO class

        Args:
            table (list of dict): 2D data structure (list of dicts) that 
            holds the data during runtime

        Returns:
            appends new entry to Inventory file
        """
        # Add data to the table
        strID, strTitle, strArtist=IO.userinput()
        intID = int(strID) 
        dicRow = {'ID':intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)

    @staticmethod
    def delete_inventory(table):
        """Function to delete CD from user input.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) 
            that holds the data during runtime
            
        Returns:
            Removes data associated to ID user input held in the table
        """
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru lstTbl and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


    @staticmethod
    def save_inventory(table):
        """Function to save CD info from user input.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) 
            that holds the data during runtime
            
        Returns:
            Save exsited data to txt file
        """
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        try:   
            while strYesNo not in ['y','n']: 
                raise ValueError('That is not a valid choice!') 
        except Exception as error:
            print('Please enter y for yes or n for no. No other inputs are valid')
            print(error)
        else:     
            if strYesNo == 'y':
            # 3.6.2.1 save data
                FileProcessor.write_file(strFileName, lstTbl)
                print('Data saved to file')
            if strYesNo=='n':
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'rb') as objFile:
                table = pickle.load(objFile)
                return table
        except FileNotFoundError:
            print("Warning: There's no file in the directory.")
        
    
    @staticmethod
    def write_file(file_name, table):
        """Function to write data to the file identified by file_name into a 2D lstTbl
       Args:
           file_name (string): name of file used to read the data from
           table (list of dict): 2D data structure (list of dicts) 
           that holds the data during runtime
           
       Returns:
           Write to file 
       """
        with open(file_name, 'wb') as objFile:
                pickle.dump(table, objFile)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        try:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']: 
                raise ValueError('That is not a valid choice!') 
        except ValueError as e:
            print(type(e))
            print('Please enter one of the offered options from menu') 
        else:   
            print("Thank you for entering a valid choise, please continue:")
            return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # Add I/O functions
    @staticmethod
    def userinput():
        """Displays guidance for user input
        Args:
            None
        Returns:
            StrID, strTitle and srArtist
        """
        #Ask user for new ID, CD Title and Artist
        ValidID = False
        while not ValidID:
           try:
               strID = int(input('Enter ID: ').strip())
               if strID <=0:
                   raise ValueError('That is not a positive integer number!') 
           except ValueError:
               print('Please enter ID using positive integers')
           else:
               ValidID=True
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # 3.3.2 Add item to the table
        IO.show_inventory(lstTbl)
        DataProcessor.add_inventory(lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        DataProcessor.delete_inventory(lstTbl)# 3.5.1.2 ask user which ID to remove # 3.5.2 search thru table and delete CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        DataProcessor.save_inventory(lstTbl)
        IO.show_inventory(lstTbl)
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')