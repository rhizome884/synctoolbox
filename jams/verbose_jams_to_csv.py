import jams
import csv
import sys

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
    # Initialise list with fieldnames
    # Variables pertaining to JAMS/SynthTab format:
    # 'value' = {'fret': integer, 'velocity': number, 'effects': dict}
    # 'sandbox' = {'string_index': int, 'open_tuning': int}
    note_data = [['start', 'duration', 'pitch', 'velocity', 'instrument',
                  'fret', 'string', 'tuning', 'effects']]
    # get note_tab annotation
    ann = jam.search(namespace='note_tab')
    # add note data to list
    for string in ann:
        for note in string:
            # Calculate note onset in seconds using initial bpm
            time = note[0]
            bpm = get_initial_bpm(jam)
            onset_in_s = onset_ticks_to_seconds(time, bpm)
            # Calculate note duration in seconds using initial bpm
            dur = note[1]
            dur_in_s = duration_ticks_to_seconds(dur, bpm)
            # Add fret and string tuning values to get midi pitch
            fret = note[2]['fret']
            open_tuning = string['sandbox']['open_tuning']
            pitch = tabnote_to_midinote(fret, open_tuning)
            # Get note velocity 
            velocity = note[2]['velocity']
            # Get string number 
            string_index = string['sandbox']['string_index']
            # Get note effects if they exist
            effects = None
            if 'effects' in note[2]:
                effects = note[2]['effects']
                for effect in effects:
                    fx_time = onset_ticks_to_seconds(effect['time'], bpm)
                    effect['time'] = fx_time
                    fx_dur = duration_ticks_to_seconds(effect['duration'], bpm)
                    effect['duration'] = fx_dur
            # Append note data to list
            note_data.append([onset_in_s, dur_in_s, pitch, velocity, instrument,
                              fret, string_index, open_tuning, effects])
    # return note data as list of lists
    return note_data

def save_note_data_list_as_csv(note_data, filename):
    # open csv file and write note data from list of lists
    with open(filename + ".csv", "w") as f:
        writer = csv.writer(f, delimiter=';')
        for row in note_data:
            writer.writerow(row)
    print(f"JAMS data written to {filename}.csv")

if __name__ == "__main__":
    # add filename for JAMS and CSV files
    filename = sys.argv[1]
    # add schema for synthtab JAMS
    jams.schema.add_namespace('note_tab.json')
    # load JAMS file
    jam = jams.load(filename + ".jams")
    # put data that is to be time warped in list
    instrument = 'guitar'
    note_data = put_note_data_in_list(jam, instrument)
    # save the list as a csv file
    save_note_data_list_as_csv(note_data, filename)
