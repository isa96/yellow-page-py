import csv
import sys
import os
import tabulate
import pyinputplus as pypi

def show(data):
    '''Function to show dataset in prompt
    
    Args:
        data (list of dictionary): dataset to show
    '''

    # Print to prompt in table format
    print(tabulate.tabulate([data[i].values() for i in range(len(data))], data[0].keys(), tablefmt='outline'))

def search():
    '''Function to search contact
    '''
    # Print notes about default condition of this feature
    print("Notes: In default this feature only search based on 'nama' and 'no_telepon' column")

    # Input value to search
    value = input('input your value : ')

    # Create list of data that contain the value
    scDataset = []
    for i in range(len(dataset)):
        if value.upper() in list(dataset[i].values())[1] or value in list(dataset[i].values())[2]:
            scDataset.append(dataset[i])
    
    # Validate the result (if value is founded then show the data, if not then print notification)
    if len(scDataset) > 0:
        show(scDataset)
    else:
        print("\nData does not exist!\n") 

def filter():
    '''Fungsi untuk memfilter dataset
    '''
    # input the key (column) that used to filter
    key = pypi.inputMenu(prompt='\nSelect column :\n', choices=header[1:], numbered=True)

    # generate all distinct list of value from the key
    listvalue = list({dataset[i][key] for i in range(len(dataset))})

    # Select the value
    value = pypi.inputMenu(prompt='\nSelect value:\n', choices=listvalue, numbered=True)

    # Create dataset from the selected value
    filterDataset = []
    for i in range(len(dataset)):
        if value in dataset[i][key]:
            filterDataset.append(dataset[i])  

    # Print the result into prompt
    show(filterDataset)

def summary():
    '''Function to show the summary of dataset 
    '''

    print(f'\nNumber of Contact : {len(dataset)}')

    # Select the key 'jenis' and 'kabupaten kota'
    key = header[3:5]

    # Create Summary from 'jenis' contact
    # Create list value of 'jenis'
    listvalue1 = list(dataset[i][key[0]] for i in range(len(dataset)))

    # Create distinct list value of 'jenis' 
    listvalue2Unique = list({dataset[i][key[0]] for i in range(len(dataset))})
    
    # Create dataset of 'jenis' contact summary
    listCount1 = []
    for i in range(len(listvalue2Unique)):
        listCount1.append([
            listvalue2Unique[i],listvalue1.count(listvalue2Unique[i])])

    # Sort Descending
    for i in range(len(listCount1)):    
        for j in range(i+1, len(listCount1)):    
            if(listCount1[i][1] < listCount1[j][1]):    
                temp = listCount1[i]    
                listCount1[i] = listCount1[j]    
                listCount1[j] = temp

    # Print the result to prompt
    print("\nNumber of Contact by Category\n")
    print(tabulate.tabulate(listCount1, [key[0],'Count of Contact'], tablefmt='outline'))

    # Create Summary from 'kabupaten_kota' contact
    # Create list value of 'kabupaten_kota'
    listvalue2 = list(dataset[i][key[1]] for i in range(len(dataset)))

    # Create distinct list value of 'kabupaten_kota' 
    listvalue2Unique = list({dataset[i][key[1]] for i in range(len(dataset))})

    # Create dataset of 'kabupaten_kontak' contact summary
    listCount2 = []
    for i in range(len(listvalue2Unique)):
        listCount2.append([
            listvalue2Unique[i],listvalue2.count(listvalue2Unique[i])])

    # Sort Descending
    for i in range(len(listCount2)):    
        for j in range(i+1, len(listCount2)):    
            if(listCount2[i][1] < listCount2[j][1]):    
                temp = listCount2[i]    
                listCount2[i] = listCount2[j]    
                listCount2[j] = temp

    # Print the result to prompt
    print("\nNumber of Contact by Regency\n")
    print(tabulate.tabulate(listCount2, [key[1],'Count of Contact'], tablefmt='outline'))   
    print('\n')

def addNormal():
    '''Function to add contact
    '''

    # Create list of value from 'jenis', 'kabkot', and id column
    listJenis = list(set(list(dataset[i].values())[3] for i in range(len(dataset))))
    listKabkot = list(set(list(dataset[i].values())[4] for i in range(len(dataset))))
    listId = [list(dataset[i].values())[0] for i in range(len(dataset))]

    # input no_telepon
    no_telepon = pypi.inputStr(prompt='input phone number :', blockRegexes=[r'[A-Za-z]'])

    # Check whether 'no_telepon' has in database or not
    datNo = []
    for i in range(len(dataset)):
        if no_telepon == list(dataset[i].values())[2]:
            print('Contact already in database :\n')
            datNo.append(dataset[i])
            break
    
    if len(datNo) > 0:
        show(datNo)
    else:
        # Input nama, jenis, and kabupaten kota value          
        nama = input('input name :').upper()
        jenis = pypi.inputMenu(prompt='input category :\n', choices=listJenis, numbered=True)
        kabKot = pypi.inputMenu(prompt='input regency :\n', choices=listKabkot, numbered=True)

        dataset.append({
            header[0] : max(listId)+1,
            header[1] : nama,
            header[2] : no_telepon,
            header[3] : jenis,
            header[4] : kabKot,
            header[5] : 'no'
        })

        # print the success message and result in prompt
        print('Data Sucessufully Added!\n')
        show(dataset)

def deleteID():
    '''Function to delete contact based on id
    '''
    # Collect id to delete
    listID  = []
    while True:
        id = input('\nInput id :')
        if id == '':
            break
        else:
            listID.append(int(id))
    listID = list(set(listID))

    # Validate listID is inputted or not
    if len(listID) == 0:
        print('No id Inputed!')
    else:
        # Checking list of id inputted on database
        print(listID)
        conData = []
        for i in listID:
            for j in range(len(dataset)):
                if i == list(dataset[j].values())[0]:
                    conData.append(dataset[j])
        
        # Valiadtion
        if len(conData) == 0:
            print('\nid not found\n')
        else:
            # Show the data that will be deleted
            show(conData)

            # Confirmation of deletion
            prompt = '\nAre you sure to delete this data ?(Y/N) :'
            con = pypi.inputYesNo(prompt=prompt)

            if con == 'yes':
                # Delete process
                for dat in dataset.copy():
                    if dat in conData:
                        dataset.remove(dat)

                print(f'{len(conData)} data deleted!\n')
                show(dataset)
            else:
                print('data not deleted!')

def deleteGroup():
    '''Function to delete contact based on category/regency
    '''
    # Select 'jenis ' and 'kabupaten kota' column
    group = header[3:5]

    # Select first column to filter value
    key1 = pypi.inputMenu(prompt='Select First Group :\n', choices=group, numbered=True)
    # Create list of value
    listvalue1 = list({dataset[i][key1] for i in range(len(dataset))})
    # Select the value
    value1 = pypi.inputMenu(prompt='Select value:\n', choices=listvalue1, numbered=True)
    # Create a dataset of filtered value
    filterDataset1 = []
    for i in range(len(dataset)):
        if value1 in dataset[i][key1]:
            filterDataset1.append(dataset[i])  
    show(filterDataset1)

    # Remove the column that used to filter befoe
    group.remove(key1)

    # Confirmation of add second column to filter
    conf = pypi.inputYesNo(prompt=f'Add Selected Group by {group[0]} (Y/N): ')

    if conf == 'yes':
        # Select the rest column
        key2 = group[0]
        # Create list of value
        listvalue2 = list({filterDataset1[i][key2] for i in range(len(filterDataset1))})
        # Select the value
        value2 = pypi.inputMenu(prompt='Select value:\n', choices=listvalue2, numbered=True)
        # Create dataset of filtered value
        filterDataset2 = []
        for i in range(len(dataset)):
            if value2 in dataset[i][key2] and value1 in dataset[i][key1]:
                filterDataset2.append(dataset[i])  
        show(filterDataset2)

        # Confirmation of deletion
        conf = pypi.inputYesNo(prompt='\nAre you sure want to delete the contact above? (Y/N)\n')
        if conf == 'yes':
            for dat in dataset.copy():
                if dat in filterDataset2:
                    dataset.remove(dat)
            show(dataset)
    else:
        # Confirmation of deletion
        conf = pypi.inputYesNo(prompt='\nAre you sure want to delete the contact above? (Y/N)\n')
        if conf == 'yes':
            for dat in dataset.copy():
                if dat in filterDataset1:
                    dataset.remove(dat)
            show(dataset)

def edit():
    '''Function to update contact
    '''
    # Create list of id
    listId = [list(dataset[i].values())[0] for i in range(len(dataset))]

    # Input id
    id = int(input('Input id :'))

    # Check id
    if id not in listId:
        print('id Not Found!')
    else:
        # Search the contact
        for i in range(len(dataset)):
            if id == list(dataset[i].values())[0]:

                print('This data will be edited :')
                show([dataset[i]])

                while True:
                    # Input the new information
                    listJenis = list(set(list(dataset[i].values())[3] for i in range(len(dataset))))
                    listKabkot = list(set(list(dataset[i].values())[4] for i in range(len(dataset))))

                    key = pypi.inputMenu(prompt='Select column to update :\n', choices=header[1:], numbered=True)
                    
                    if key == header[1]:
                        val = input('input name :').upper()
                    elif key == header[2]:
                        val = pypi.inputStr(prompt='input phone number :', blockRegexes=[r'[A-Za-z]'])
                    elif key == header[3]:
                        val = pypi.inputMenu(prompt='input category :\n', choices=listJenis, numbered=True)
                    elif key == header[4]:
                        val = pypi.inputMenu(prompt='input regency :\n', choices=listKabkot, numbered=True)
                    else:
                        val = pypi.inputYesNo(prompt='bookmark this contact?(Y/N) :')

                    # Show Before After
                    print('Before :')
                    show([dataset[i]])

                    dataset[i][key] = val

                    print('\nAfter')
                    show([dataset[i]])

                    # Move the bookmarked contact to first order
                    if key == header[5] and val == 'yes':
                        dataset.insert(0,dataset.pop(i))
                    
                    # Confirmation to continue edit
                    contEdit = pypi.inputYesNo(prompt='Continue edit?(Y/N) :')
                    if contEdit == 'no':
                        break
        
        show(dataset)

def main():
    '''Main program to run whole process
    '''
    global dataset

    while True:
        print('\n=== Welcome to Yogyakarta IMPORTANT Contact System ===\n')
        prompt = f'Please select menu :\n'
        choice = ['Show Contact', 'Add Contact', 'Delete Contact', 'Edit Contact', 'Exit']

        response = pypi.inputMenu(prompt=prompt, choices=choice, numbered=True)

        if response == choice[0]:
            show(dataset)
            while True:
                choiceDisp = ['Show All','Search','Filter','Summary','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    show(dataset)
                if respDisp == choiceDisp[1]:
                    search()
                elif respDisp == choiceDisp[2]:
                    filter()
                elif respDisp == choiceDisp[3]:
                    summary()
                else:
                    break
        elif response == choice[1]:
            while True:
                choiceDisp = ['Add New Contact','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    addNormal()
                else:
                    break
        elif response == choice[2]:
            while True:
                choiceDisp = ['Delete Based on ID','Delete Based on Category/Regency','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    deleteID()
                elif respDisp == choiceDisp[1]:
                    deleteGroup()
                else:
                    break     
        elif response == choice[3]:
            while True:
                choiceDisp = ['Update Data','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    edit()
                else:
                    break
        else:
            break

    file = open(path, 'w', newline = '')

    writer = csv.writer(file, delimiter=';')

    datasetVal = [header]
    for i in range(len(dataset)):
        datasetVal.append(dataset[i].values())

    writer.writerows(datasetVal)

    file.close()

if __name__ == "__main__":
    # define path (file stored location)
    path = pypi.inputFilepath(prompt='Input your File (important_number_jogja.csv) path : ')

    # Check empty files
    if os.path.getsize(path) == 0:
        print("Database is empty, please enter available contact first")
    else:
        # import databse file
        file = open(path)
        # read data from database file
        reader = csv.reader(file, delimiter=';')

        # create header
        header = next(reader)

        # check header
        headerRules = ['id', 'name', 'phone number', 'category', 'regency', 'bookmark']

        if len(header) == 0:
            print("Your database does not have header, please check your files")
            print(f"Make sure you have header with the following column:\nid;name;phone number;category;regency;bookmark")
        # check if header meet the rules
        elif header != headerRules:
            print("Your database's header doesnt match with the format rules, please check your files")
            print(f"Make sure you have header with the following column:\nid;name;phone number;category;regency;bookmark")
        else:
            # create list of dictionary from database
            dataset = []
            for row in reader:
                if len(row) == 0:
                    continue
                else:
                    if 'yes' in row[5]:
                        dataset.insert(0,{
                            header[0] : int(row[0]),
                            header[1] : str(row[1]).upper(),
                            header[2] : str(row[2]),
                            header[3] : str(row[3]).lower(),
                            header[4] : str(row[4]).lower(),
                            header[5] : str(row[5])
                        })
                    else:
                        dataset.append({
                            header[0] : int(row[0]),
                            header[1] : str(row[1]).upper(),
                            header[2] : str(row[2]),
                            header[3] : str(row[3]).lower(),
                            header[4] : str(row[4]).lower(),
                            header[5] : str(row[5])
                        })

            # close the database file
            file.close()

            # Run main program
            main()

    # Close the program
    sys.exit()