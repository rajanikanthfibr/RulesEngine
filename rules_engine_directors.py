import requests
import json
auth_cred=('yh2Now9JlNe30cbCFd5g1jTkCk9XqR9O1zQ11KRS', '')

def company_directors(company_number):
    '''
    Function to return the list of directors for a company id
    '''
    url='https://api.companieshouse.gov.uk/company/'+str(company_number)+'/officers'
    r = requests.get(url,
                 auth=auth_cred)
    j = r.json()
    director_id=[]
    for doc in j['items']:
        if doc['officer_role']=='director':
            temp=doc['links']['officer']['appointments']
            temp=temp.replace('/officers/','')
            temp=temp.replace('/appointments','')
            director_id.append(temp)
    return director_id


def insolvency_dates(company_no):
    '''
    Function to get check if the company status is not in Dissolved, Active, Open, Closed, Converted/Closed
    and get the cessation date

    '''

    url = 'https://api.companieshouse.gov.uk/company/' + company_no + '/insolvency'
    r = requests.get(url,
                     auth=auth_cred)
    j = r.json()
    try:
        case = j['cases']
        return next(item for item in case[0]['dates'] if item["type"] == "wound-up-on")['date']
    except:
        pass


# Get all the company numbers and resignation dates (if they resigned) by the above director ids
def get_company_details(director_id):
    '''
    Function to return the list of all the companies that have the given directors and their resignation dates
    (if resigned)

    '''
    from datetime import datetime, timedelta
    url = 'https://api.companieshouse.gov.uk/officers/' + director_id + '/appointments'
    r = requests.get(url,
                     auth=auth_cred)
    j = r.json()

    insolvency_flag = False
    details = []

    for doc in j['items']:

        # Check the role of director
        if doc['officer_role'] == 'director':

            company_no = doc['appointed_to']['company_number']

            try:

                # Get the date when company went into insolvency
                insolvency_date = insolvency_dates(company_no)

                # Convert to datetime
                insolvency_date = datetime.strptime(insolvency_date, '%Y-%m-%d').date()

                today_date = datetime.today().strftime('%Y-%m-%d')
                today_date = datetime.strptime(today_date, '%Y-%m-%d').date()
                num_months_from_today = (today_date.year - insolvency_date.year) * 12 + (
                            today_date.year - insolvency_date.year)

            except:
                pass

            if 'resigned_on' in doc:

                # Get the resigned date
                resigned_date = doc['resigned_on']
                # Convert to datetime
                resigned_date = datetime.strptime(resigned_date, '%Y-%m-%d').date()

                try:

                    # Check if the insolvency_date is in last 5 years or in 12 months after resignation
                    num_months_from_resignation = (insolvency_date.year - resigned_date.year) * 12 + (
                                insolvency_date.year - resigned_date.year)
                    if (num_months_from_today < 60) and (num_months_from_today > 0) and (num_months_from_resignation < 12):
                        insolvency_flag = True

                    details.append([company_no, resigned_date, insolvency_date, flag])
                except:
                    pass
            else:
                try:
                    # Check if the insolvency_date is in last 5 years
                    if (num_months_from_today < 60) and (num_months_from_today > 0):
                        insolvency_flag = True
                except:
                    pass

    return insolvency_flag, details

def get_insolvency_flag(company_number):
    '''
    Final function to get insolvency flags for the directors of the company
    '''
    # Get the list of directors
    directors=company_directors(company_number)
    flag= False
    for director in directors:
        if get_company_details(director)[0]==True:
            flag=True
    return flag

