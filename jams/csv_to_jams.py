import csv
import jams

# CSV data

# Read csv data
with open('test_m-carcassi_andantino_dtw.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    note_list = list(reader)

# Remove header
note_list.pop(0)


# JAMS experiments

# Add schema for synthtab JAMS
jams.schema.add_namespace('note_tab.json')

# Load JAMS data
jam = jams.load("test_m-carcassi_andantino.jams")

# Load note_tab data
note_tabs = jam.search(namespace='note_tab')

# Create a count variable to check number of JAMS note events
jam_note_count = 0

# Add note events from each guitar string
for note_tab in note_tabs:
    jam_note_count += len(note_tab['data'])

# See if the same number of notes are in both data structures 
if jam_note_count == len(note_list):
    print("Same number of notes in JAMS and list objects")
else:
    print("Different number of notes in JAMS and list objects")

i = 0

while i < jam_note_count:
    for note_tab in note_tabs:
        for data in note_tab:
            time = note_list[i][0]
            dur = note_list[i][1]
            value = data[2]
            conf = data[3]
            print(data)
            data = (time, dur, value, conf)
            print(data)
            print(i)
            i += 1

