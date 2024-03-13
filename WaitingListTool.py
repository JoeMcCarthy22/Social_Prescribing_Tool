# Welcome to the Social Prescribing Waiting List Tool!
# This programme is intended to signpost patients to local services whilst they wait for an appointment

# This programme reads a database file (waiting list) and uses OOP to tailor suggestions for the individual


# create a class to store information about the Patient
class Patient:
    '''Creates a class for a patient'''

    def __init__(self, waiting_position, nhs_number, email, age):
        self.waiting_position = waiting_position
        self.nhs_number = nhs_number
        self.email = email
        self.age = int(age) if age.isdigit() else None  # Convert to int only if age is a digit

    def __str__(self):
        return f"Waiting Position: {self.waiting_position}, NHS Number: {self.nhs_number}, Email: {self.email}, Age: {self.age}"

# create a waiting list container to store all the patients
waiting_list = []

# initialise class and add each patient to the waiting list

def populate_waiting_list():
    ''' reads the text file,
    instantiates each line as a seperate Patient class
    adds to waiting list'''

    with open("inbound_referrals.txt", "r") as file:
        for line in file:
            # Split the line into fields
            fields = line.strip().split(',')

            # extract values from the fields
            waiting_position = fields[0]
            nhs_number = fields[1]
            email = fields[2]
            age = fields[3]

            # Create an instance of Patient and add it to the waiting list
            patient = Patient(waiting_position, nhs_number, email, age)
            waiting_list.append(patient)

populate_waiting_list()

# create a function to consider user's housebound status 

def change_housebound_status(user):
    while True:
        housebound_answer = input("\nIn order to tailor your experience, please answer: are you housebound? (yes/no)\n").lower()
        if housebound_answer == 'no':
            print("You have been listed as not being housebound")
            break
        elif housebound_answer == 'yes':
            print("You are listed as being housebound")
            break
        else:
            print("Sorry - input not recognised - please check your spelling and try again.")    
        
    return housebound_answer

# *********** MAIN MENU FUNCTIONS *****************
# These functions are later called within the main menu of the programme

# function for housing support
def housing_support():
    print("You have selected housing\n")
    if user.age >= 50:
        print("AgeUK Ealing can assist with housing. "
              "Website: https://www.ageuk.org.uk/ealing/our-services/information-advice-3677b7fd-87e4-eb11-ba5e-00155d585af3/\n")
    elif user.age < 50:
        print("Ealing Advice Service can assist with housing. Website: https://ealingadvice.org/\n")

# function for benefits support
def benefits_support():
    print("You have selected benefits.\nTurn2Us online calculator is highly recommended.")
    if user.age >= 50:
        print("Alternatively, if you require additional support, AgeUK Ealing can assist with benefits."
              "Website: https://www.ageuk.org.uk/ealing/our-services/information-advice-3677b7fd-87e4-eb11-ba5e-00155d585af3/\n")
    elif user.age < 50:
        print("Alternatively, if you require additional support, Ealing Advice Service can assist with benefits. Website: https://ealingadvice.org/\n")

# function for mental health support
def mental_health_support():
    print("""For free therapy you can self-refer online to NHS talking therapies.
          Alternatively, if you are feeling as if you are approaching a crisis point, Single Point of Access (SPA) can assist
          Contact Details:
          Talking Therapies: nhs.uk/mental-health/talking-therapies-medicine-treatments/talking-therapies-and-counselling/nhs-talking-therapies
          SPA: westlondon.nhs.uk/our-services/adult/mental-health-services/single-point-access#:~:text=The%20Mental%20Health%20Single%20Point,our%20trained%20mental%20health%20advisors. """)

# function for social isolation/ loneliness support
def social_isolation_support(user, housebound_answer):
    if housebound_answer == 'yes':
        print("As you have declared yourself to be housebound, I would recommend BEfriend, who offer telephone befriending services. Website: BEfriend.london\n")
    else: print("As you have declared yourself to not be housebound, I recommend Mindfood, who run group gardening sessions locally - Website: Mindfood.org.uk\n")


######### Validation of user #########
# email address is used to validate the user
# user object is then created in the Patient class 

while True: 
# validate that the user is on the waiting list via email
    validation_email = input("Please confirm your email address in order to proceed\n")

    # Search for user details in the waiting list
    user = None
    for patient in waiting_list:
        if validation_email == patient.email:
            user = patient
            break

    # Check if user details are found
    if user is not None:
        print(f"""User details found: {user}\n
Welcome to the Social Prescribing Waiting List.
This program will send you suggestions for local groups and services to address the issues in your referral.
You will be offered an appointment when there is availability.""")
        break 
    else:
        print("Sorry, email address not recognized. Please try again.")


######  Main menu for the tool #######
        

# request housebound status from the user 
housebound_answer = change_housebound_status(user)

while True:
    menu_choice = input("""Please select an option from the following:
        1: Housing
        2: Benefits
        3: Mental Health
        4: Social Isolation/Loneliness
        5: Change Housebound status
        6: Exit
        
Please enter the respective number to proceed:
""").strip(":")
    
    if menu_choice == '1':
        housing_support()
    
    elif menu_choice == '2':
       benefits_support()
    
    elif menu_choice == '3':
        mental_health_support()
    
    elif menu_choice == '4':
        social_isolation_support(user, housebound_answer)
    
    elif menu_choice == '5':
        housebound_answer = change_housebound_status(user)
    
    elif menu_choice == '6':
        print("""\nThank you for using the Social Prescribing Waiting list tool.
You will be contacted when we have availability for an appointment.
In the meantime we suggest you look into the services shared today.""")
        break

    else: 
        print("Sorry - input not recognised - please check your spelling and try again.")   
    


