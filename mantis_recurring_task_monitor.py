#!/usr/bin/python

import argparse
import json
import requests
import datetime
import dateutil.parser
import pytz

parser = argparse.ArgumentParser(description='Manage recurring tasks in Mantis')
parser.add_argument('--api', help='URL to Mantis REST API', required=True)
parser.add_argument('--token', help='Mantis API token', required=True)
parser.add_argument('--project', help='Project containing recurring ticket masters', required=True)

args = parser.parse_args()

headers = { 'Authorization': args.token }
post_headers = { 'Authorization': args.token, 'Content-Type': 'application/json' }

r_proj = requests.get(args.api + '/projects', headers=headers)

project_id = -1
for project in r_proj.json()['projects']:
    if project['name'] == args.project:
        project_id=project['id']

if project_id == -1:
    print json.dumps(r_proj.json(), indent=2)
    raise Exception("Failed to find a matching project name.")

print "Project ID: " + str(project_id)

r_seed = requests.get(args.api + '/issues/?project_id=' + str(project_id), headers=headers)
#print json.dumps(r_seed.json(), indent=2)

for seed in r_seed.json()['issues']:
    if seed['status']['name'] in ['resolved', 'closed']:
        print "Skipping seed issue " + str(seed['id']) + " due to state = " + seed['status']['name']
        continue
    print "Seed " + str(seed['id']) + ":"
    instance_project = ""
    recur_days = -1
    remind_days = -1
    for custom in seed['custom_fields']:
        if custom['field']['name'] == "Instance Project":
            instance_project = custom['value']
        elif custom['field']['name'] == "Recur Days":
            recur_days = int(custom['value'])
        elif custom['field']['name'] == "Remind Days":
            remind_days = int(custom['value'])
    last_update_all = dateutil.parser.parse("1970-01-01T00:00:00-05:00")
    last_update = -1
    last_update_open = dateutil.parser.parse("1970-01-01T00:00:00-05:00") 
    last_open = -1
    for rel in seed['relationships']:
        if rel['type']['name'] == "has instance":
            r_rel = requests.get(args.api + '/issues/' + str(rel['target_id']), headers=headers)
            issue = r_rel.json()["issues"][0]
            updated = dateutil.parser.parse(issue["updated_at"])
            if updated > last_update_all:
                last_update_all = updated
                last_update = issue['id']
            if issue['status']['name'] != 'closed' and updated > last_update_open:
                last_update_open = updated
                last_open = issue['id']
            print json.dumps(r_rel.json(), indent=2)
    print "  Last Updated Instance was " + str(last_update) + " at " + str(last_update_all)
    print "  Last Open Updated Instance is " + str(last_open) + " at " + str(last_update_open)
    if remind_days > 0 and last_open != -1 and datetime.datetime.now(pytz.utc) > last_update_open + datetime.timedelta(days=remind_days):
        # if we have an open instance, and the reminder interval has expired
        print "We need to update " + str(last_open) + " with a reminder note"
        note = {'text': "This is a reminder to complete this recurring task." }
        r_note = requests.post(args.api + '/issues/' + str(last_open) + '/notes', headers=post_headers, data=json.dumps(note))
        print r_note.text
    if recur_days > 0 and last_open == -1 and last_update != -1 and datetime.datetime.now(pytz.utc) > last_update_all + datetime.timedelta(days=recur_days):
        # if we have a closed instance, and the recur interval has expired based on its last update
        print "We need to create a new instance for seed " + str(seed['id'])

    
