import ldap 
import time
from rich import print as rprint
from rich.prompt import Prompt

def calculate_control_number(id_number: str) -> int:
    """
    Calculates the control number for the given Estonian national identification number.
    Info about the algorithm: https://et.wikipedia.org/wiki/Isikukood#Kontrollnumber

    Args:
        id_number (int): Estonian national identification number without the control number

    Returns:
        int: Control number
    """
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    weighted_sum = sum(int(id_number[i]) * weights[i] for i in range(10))
    remainder = weighted_sum % 11
    if remainder < 10:
        return remainder
    weights = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    weighted_sum = sum(int(id_number[i]) * weights[i] for i in range(10))
    remainder = weighted_sum % 11
    if remainder < 10:
        return remainder
    return 0

def get_first_nr(gender, dob):
    """
    Gets the first number of the identification number.
    More info: https://et.wikipedia.org/wiki/Isikukood#Sugu

    Args:
        gender: Gender of the person (m/f)
        dob: Date of birth of the person (YYMMDD)
    
    Returns:
        int: First number of the identification number
    """
    year = int(dob[0:2])
    if gender == "m":
        if year > 23:
            return 3
        return 5
    if year > 23:
        return 4
    return 6

def generate_ids(gender, dob):
    """
    Generates all possible ID candidates based on gender and DOB.

    Args:
        gender (m/f): Gender of the person
        dob (YYMMDD): Date of birth of the person
    
    Returns:
        list: List of all possible ID candidates
    """
    intervals = [(1, 5), (11, 15), (21, 85), (151, 156), (161, 190), (221, 240), (271, 320), (371, 400), (421, 450), (471, 485), (491, 510), (521, 540), (571, 585), (601, 620), (651, 670)]
    possible_ids = list()
    n1 = str(get_first_nr(gender, dob))
    for i in range(1, 701):
        for invl in intervals:
            if i in range(invl[0], invl[1]):
                id = n1 + dob + "{:03d}".format(i)
                id += str(calculate_control_number(id))
                possible_ids.append(id)
    return possible_ids

def spam_api(possible_ids):
    """
    Spams the SK API with all possible ID candidates and returns the hits.
    
    Args:
        possible_ids (list): List of all possible ID candidates
    
    Returns:
        list: List of all hits
    """
    hits = list()
    ldap_server_url = 'ldaps://esteid.ldap.sk.ee/'
    bind_dn = 'c=EE'
    bind_pw = ''
    base_dn = 'c=EE'
    counter = 1
    for id_ in possible_ids:
        x = int(id_[7:10])
        search_filter = f'(serialNumber=PNOEE-{id_})'
        conn = ldap.initialize(ldap_server_url)
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        try:
            res = result[0][0]
            res = res.split(',')
            for i in res:
                if 'o=' in i:
                    res = i.replace('o=', '')
            if res == 'Identity card of Estonian citizen':
                res = '[dodger_blue1]' + '[' + res
            if res == 'Identity card of European Union citizen':
                res = '[yellow3]' + '[' + res
            if res == 'Digital identity card of e-resident':
                res = '[dark_orange3]' + '[' + res
            if res == 'Residence card of long-term resident':
                res = '[dark_cyan]' + '[' + res
            if res == 'Residence card of temporary residence citizen':
                res = '[chartreuse1]' + '[' + res
            if res == 'Mobile-ID':
                res = '[violet]' + '[' + res
            line = (f'[[white]{counter}/{len(possible_ids)}] {result[1][1]["cn"][0].decode("utf8").replace(",", ", ")} {res}]')
            rprint(line)
            hits.append(result[1][1]["cn"][0])
        except:
            pass
        conn.unbind()
        time.sleep(0.1)
        counter += 1
    return hits

def main():
    try:
        dob = Prompt.ask("[white][bold]Enter target date of birth (YYMMDD)[/bold]\n")
        if len(dob) != 6:
            rprint('[red1][bold]Invalid DoB, exiting.[/bold]')
            return
        print("")
        gender = Prompt.ask("[bold]Enter target gender (m/f)[/bold]\n")
        if gender != 'm' and gender != 'f':
            rprint('[red1][bold]Invalid gender, exiting.[/bold]')
            return
        print("")
        search = Prompt.ask("[bold]Enter search term (leave empty for none)[/bold]\n")
        print("")

        births = spam_api(generate_ids(gender, dob))

        print("")

        if search != "":
            matches = list()
            for i in births:
                if search.lower() in str(i.decode("utf8").lower()):
                    matches.append(i)
            if len(matches) == 0:
                rprint("[bold]Person matching search term not found[/bold].")
            if len(matches) != 0:
                rprint("[bold]Match(es) found:[/bold]")
                for match in matches:
                    rprint(f'[bold]{match.decode("utf8").replace(",", ", ")}[/bold]')
        return
    except KeyboardInterrupt:
        print('')
        print('Keyboard interrupt, exiting.')

main()
