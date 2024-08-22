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
    # set offset so onset of bar-1-beat-1 notes start at 0s
    start_offset = 960
    # convert ticks to seconds and return float
    return (60 / (bpm * ppq)) * (ticks - start_offset)

def tabnote_to_midinote(fret, open_tuning):
    # add string tuning (open_tuning) midi pitch value
    # and fret number, then return midi pitch value
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

def put_note_data_in_list(jam, instrument):
    # initialise list with fieldnames 
    note_data = [['start', 'duration', 'pitch', 'velocity', 'instrument']]
    # get note_tab annotation
    ann = jam.search(namespace='note_tab')
    # add note data to list
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
            note_data.append([onset_in_s, dur_in_s, pitch, velocity, instrument])
    # return note data as list of lists
    return note_data

def save_note_data_list_as_csv(note_data, filename):
    # open csv file and write note data from list of lists
    with open(filename + ".csv", "w") as f:
        writer = csv.writer(f, delimiter=';')
        for row in note_data:
            writer.writerow(row)
    print(f"Note data written to {filename}.csv")

if __name__ == "__main__":
    # add filename for JAMS and CSV files
    filename = 'm-carcassi_andantino'
    # add schema for synthtab JAMS
    jams.schema.add_namespace('note_tab.json')
    # load JAMS file
    jam = jams.load(filename + ".jams")
    # put data that is to be time warped in list
    instrument = 'guitar'
    note_data = put_note_data_in_list(jam, instrument)
    # save the list as a csv file
    save_note_data_list_as_csv(note_data, filename)
