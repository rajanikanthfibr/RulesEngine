import requests
import json
auth_cred=('yh2Now9JlNe30cbCFd5g1jTkCk9XqR9O1zQ11KRS', '')


def ineglible(company_no):
    url = 'https://api.companieshouse.gov.uk/company/' + str(company_no)
    r = requests.get(url,
                     auth=auth_cred)
    inelgible = False
    j = r.json()

    if ('company_number' in j) and (j['company_number'][:2] in ['CE', 'CS', 'TP', 'SL']):
        inelgible = True

    if ('type' in j) and (j['type'] in ['private-limited-guarant-nsc', 'private-limited-guarant-nsc-limited-exemption',
                                        'charitable-incorporated-organisation',
                                        'scottish-charitable-incorporated-organisation',
                                        'industrial-and-provident-society', 'private-unlimited',
                                        'private-unlimited-nsc',
                                        'scottish-partnership', 'plc'
                                        ]):
        inelgible = True

    if ('subtype' in j) and (j['subtype'] in ['community-interest-company']):
        inelgible = True

    return inelgible