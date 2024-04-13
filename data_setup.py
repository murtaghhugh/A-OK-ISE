#module used to check whether files exists and delete files 
import os


def cominput():
    """This menu allows users to navigate all other functions smoothly"""
    com = input("\nWhat would you like to do?\n\n\
     1:Build a new timetable\n\
     2:View current timetable\n\
     3:Quit\n\nEnter: ")
    #if input isn't one of the three options function is recalled
    if com == "1":
        new_data_file()
    elif com == "2":
        data_viewer()
    elif com == "3":
        print("\nThanks for using our timetable making system!\nPlease visit our site if you\'re having any issues\nHave a nice day!")
    else:
        print("\nInput not an option please try again\n\n")
        cominput()
        
            



def new_data_file():
    """new_data_file builds a csv file to store user timetables
    for each input it makes sure it is a legitimate option
    so as to avoid useless data and future causes of error"""
    #checks if file exists
    if os.path.exists("a_ok_data.csv"):
        #checks to make sure user wishes to delete old file
        my_check = input("\nYou already have a timetable\nWould you like to...\n1.Continue and replace it\n2.Cancel\nEnter: ")
        while my_check not in ["1", "2"]:
            print("Please enter either 1 or 2")
            my_check = input("\nYou already have a timetable\nWould you like to...\n\n1.Continue and replace it\n2.Cancel\n\nEnter: ")
        if my_check == "2":
            ret = input("\nPress enter to return to main menu: ")
            cominput()
            return
        else:
            os.remove("a_ok_data.csv")

    #loops through these days as they all have 6 classes
    for i in ["mon", "tue", "wed", "thur"]:
        #sets counter equal to one
        counter = 1
        #in range of 6
        for x in range(1, 7):
            #takes input for class name, teacher name and teacher email
            class_name = input(f"{i.title()} class {counter} subject: ").title()
            teacher_name = input(f"{i.title()} class {counter} teacher: ")
            teacher_email = input(f"{i.title()} class {counter} teacher email: ")

            #prints out inputed info and checks whether it is correct
            print(f"\n{i.title()} class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
            check = input("\n\nIs this correct...y/n: ").lower().strip()
            while check.lower() not in ["y", "n"]:
                print("Please enter y or n!")
                print(f"\n{i.title()} class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
                check = input("\nIs this correct...y/n: ").lower().strip()
            #if user says it is incorrect input code is repeated
            while check == "n":
                class_name = input(f"\n{i.title()} class {counter} subject: ").title()
                teacher_name = input(f"{i.title()} class {counter} teacher: ")
                teacher_email = input(f"{i.title()} class {counter} teacher email: ")
                print(f"\n{i.title()} class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
                check = input("\n\nIs this correct...y/n: ").lower().strip()
                while check.lower() not in ["y", "n"]:
                    print("Please enter y or n!")
                    print(f"\n{i.title} class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
                    check = input("\nIs this correct...y/n: ").lower().strip()
            
            #if file doesn't exist new one is made else it appends to existing file
            #writes line of code containing inputed info and then closes file           
            f= open("a_ok_data.csv","a+")
            f.write(f"{i}, {class_name}, {teacher_name}, {teacher_email}\n")
            f.close()
            #adds 1 to the counter to stop code after 6 iterations
            counter += 1
    #same process but with four class friday
    fri_counter = 1
    for i in range(1, 5):
        counter = 1
        class_name = input(f"Fri class {counter} subject: ").title()
        teacher_name = input(f"Fri class {counter} teacher: ")
        teacher_email = input(f"Fri class {counter} teacher email: ")
        print(f"\nFri class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
        check = input("\n\nIs this correct...y/n: ").lower().strip()
        while check.lower() not in ["y", "n"]:
            print("Please enter y or n!")
            print(f"\nFri class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
            check = input("\nIs this correct...y/n: ").lower().strip()
        while check == "n":
            class_name = input(f"\nFri class {counter} subject: ").title()
            teacher_name = input(f"Fri class {counter} teacher: ")
            teacher_email = input(f"Fri class {counter} teacher email: ")
            print(f"\nFri class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
            check = input("\n\nIs this correct...y/n: ").lower().strip()
            while check.lower() not in ["y", "n"]:
                print("Please enter y or n!")
                print(f"\nFri class {counter}\nClass: {class_name}   Teacher: {teacher_name}   Email: {teacher_email}")
                check = input("\nIs this correct...y/n: ").lower().strip()
                        
        f= open("a_ok_data.csv","a+")
        f.write(f"fri, {class_name}, {teacher_name}, {teacher_email}\n")
        f.close()
        fri_counter += 1

    #notifies the user that the file is finished running and returns them to the main menu
    print("All classes inputted")
    ret = input("\nPress enter to return to main menu: ")
    cominput()

def data_viewer():
    """Gives users the option to view timetable 
    in command prompt
    """
    #checks whether file exists
    if os.path.exists("a_ok_data.csv"):
        #if so sets list of all classes from other function
        all_classes = class_maker()
        #prints start of formated timetable
        print("\nHere is your current timetable:\n")
        row = "|{:15}|{:20}|{:25}|{:35}|"
        print("\n{:=^100}".format(" Class Timetable "))
        print(row.format("Day", "Class", "Teacher", "Email"))
        print("=" * 100)
        #sets counter to be used for class no.
        counter = 1
        #for loop loops through each class
        for i in range(0,len(all_classes)):
            #if statement makes sure counter does not go above 6
            if counter == 7:
                counter = 1
            #formats line of table with class information
            print(row.format(f"{all_classes[i][0].title()}  class {counter}", all_classes[i][1],  all_classes[i][2], all_classes[i][3]))
            #prints seperating line
            print("=" * 100)
            #adds to counter
            counter += 1
    else:
        #if not then user is informed that they have not yet made a timetable
        print("\nYou don\'t yet have a timetable!\nPlease make one and try again")
    #input used to pause code until user i ready
    ret = input("\nPress enter to return to main menu: ")
    #menu is called back
    cominput()


    
def class_maker():
    """Splits data file into seperate lists"""
    my_classes = []
    f= open("a_ok_data.csv","r")
    #for each line in data file code reads it splits it and appends siubsequent list to my_classes
    for line in f:
        a_class = line.split(",")
        for i in range(0, len(a_class)):
            a_class[i] = a_class[i].strip()
        my_classes.append(a_class)
    f.close()
    #returns my_classes for assignement to variable in other function
    return my_classes




#prints welcome message
print("\n\n\nWelcome to A-Ok\'s \nCommand Line Interface\n")
#calls menu
cominput()