# Get EBird Checklist observations
import csv
import json
import requests
import sys
from dotenv import dotenv_values

# Get env vars
config = dotenv_values()


def write_list_of_dict_to_csv(input_records:list, field_names:list, output_csv_file_name:str):
    '''Outputs a CSV file for a list of dictionaries, with given field-names'''

    with open(output_csv_file_name, mode='w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, extrasaction='ignore', fieldnames=field_names)
        writer.writeheader()
        writer.writerows(input_records)


def prep_output_event(checklist):
    """Prep the event table
    
    :param checklist: list - List of dict, including project-event returned by ebird. 
    :return: list - List of one dict, with information about the checklist partly-parsed for an EMu event
    """

    event_out = {}

    event_out['projId'] = checklist['projId']
    event_out['subId'] = checklist['subId']
    event_out['protocolId'] = checklist['protocolId']
    event_out['locId'] = checklist['locId']
    event_out['durationHrs'] = checklist['durationHrs']
    event_out['allObsReported'] = checklist['allObsReported']
    event_out['comments'] = checklist['comments']
    event_out['creationDt'] = checklist['creationDt']
    event_out['effortDistanceKm'] = checklist['effortDistanceKm']
    event_out['submissionMethodCode'] = checklist['submissionMethodCode']
    event_out['submissionMethodVersion'] = checklist['submissionMethodVersion']
    event_out['checklistId'] = checklist['checklistId']
    event_out['userDisplayName'] = checklist['userDisplayName']

    return [event_out]


def prep_output_obs(checklist):
    """Prep the observation table
    :param checklist: list - List of dict, including observations returned by ebird. 
    :return: list - List of dict, with additional protocol and location info for each observation
    """

    checklist_out = []

    for obs in checklist['obs']:
        obs['protocolId'] = checklist['protocolId']
        obs['locId'] = checklist['locId']
        obs['checklistId'] = checklist['checklistId']
        obs['userDisplayName'] = checklist['userDisplayName']

        checklist_out.append(obs)

    return checklist_out


def get_ebird_checklist(checklist_id):
    """
    Retrieve the observations for a given checklist id

    :param: checklist_id str - A checklist submission i.d., e.g. "S196904601"
    :return: 
    """

    ebird_key = config['EBIRD_API_KEY']

    ebird_url = f"https://api.ebird.org/v2/product/checklist/view/{checklist_id}"

    checklist_obs = requests.get(url = ebird_url,
                                 headers = {'X-eBirdApiToken':ebird_key}
                                 )
    
    if checklist_obs.status_code != 200:

        return f"ERROR -- returned {checklist_obs.status_code} -- Confirm checklist ID {checklist_id}"
    
    else:

        checklist = json.loads(checklist_obs.text)

        return checklist

    
def main(checklist_id):
    """main function"""

    checklist_out = get_ebird_checklist(checklist_id)

    checklist_obs = prep_output_obs(checklist_out)

    checklist_event = prep_output_event(checklist_out)

    # Output
    print(checklist_obs[0])

    write_list_of_dict_to_csv(
        input_records = checklist_event,
        field_names = checklist_event[0].keys(),
        output_csv_file_name = f"output/{checklist_id}_event.csv"
        )

    write_list_of_dict_to_csv(
        input_records = checklist_obs,
        field_names = checklist_obs[0].keys(),
        output_csv_file_name = f"output/{checklist_id}_obs.csv"
        )

    
if __name__ == "__main__":
    main(sys.argv[1])