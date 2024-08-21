import jams
import csv

def duration_ticks_to_seconds(ticks, bpm):
    # set pulses per second to match guitarpro 
    ppq = 960
    # convert ticks to seconds and return float
    return (60 / (bpm * ppq)) * ticks

def onset_ticks_to_seconds(ticks, bpm):
    # set pulses per second to match guitarpro 
    ppq = 960
    # set offset so initial notes start at 0 seconds
    start_offset = 960
    # convert ticks to seconds and return float
    return (60 / (bpm * ppq)) * (ticks - start_offset)

def tabnote_to_midinote(fret, open_tuning):
    # calculate and return the midi pitch value
    return fret + open_tuning

# Replace this with get_bpm() to account for tempo changes 
def get_initial_bpm(jam):
    # get tempo annotation
    ann = jam.search(namespace='tempo')
    for data in ann:
        for bpm in data:
            if bpm[0] == 0.0:
                initial_bpm = bpm[2]
    return initial_bpm

def put_note_data_in_dict(jam):
    note_data = {
            "start": [],
            "duration": [],
            "pitch": [],
            "velocity": []
            }
    # get note_tab annotation
    ann = jam.search(namespace='note_tab')
    for note in ann:
        for data in note:
            time = data[0]
            dur = data[1]
            fret = data[2]['fret']
            velocity = data[2]['velocity']
            open_tuning = note['sandbox']['open_tuning']
            pitch = tabnote_to_midinote(fret, open_tuning)
            bpm = get_initial_bpm(jam)
            onset_in_s = onset_ticks_to_seconds(time, bpm)
            dur_in_s = duration_ticks_to_seconds(dur, bpm)
            note_data["start"].append(onset_in_s)
            note_data["duration"].append(dur_in_s)
            note_data["pitch"].append(pitch)
            note_data["velocity"].append(velocity)
    return note_data

def save_note_data_dict_as_csv(note_data, filename):
    with open(filename + ".csv", "w") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(note_data.keys())
        for i in range(len(note_data.keys())):
            writer.writerow([val[i] for val in note_data.values()])

if __name__ == "__main__":
    filename = 'm-carcassi_andantino'
    # schema for synthtab JAMS
    jams.schema.add_namespace('note_tab.json')
    # load JAMS file
    jam = jams.load(filename + ".jams")
    # place synctoolbox-dtw relevant note data in dictionary
    note_data = put_note_data_in_dict(jam)
    print(note_data)
    # save the dictionary data as a csv file
    save_note_data_dict_as_csv(note_data, filename)
