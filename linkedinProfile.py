from lILogin import LILogin

def getLIProfileDetails(profileLink):
    liLogin = LILogin()
    liLogin.setup_method()    
    details = liLogin.runLILogin(url=profileLink)
    liLogin.teardown_method()

    # return details
    if(details != []):
        print(details)
    else:
        for d in details: 
            print(f'Name: {d[0]}')
            print(f'Title: {d[1]}')
            print(f'About: {d[2]}')

profileLink = input("Please enter the link to the LinkedIn profile: ")
getLIProfileDetails(profileLink)