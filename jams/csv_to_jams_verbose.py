import jams
import librosa
import csv

"""
Create a function and script that converts time warped symbolic music data
in CSV format to the JAMS format.

CSV Column Index:
    0: start (note onset time is seconds)
    1: duration (note duration in seconds)
    2: pitch (MIDI note number, 0-127)
    3: velocity (MIDI velocity number, 0-127)
    4: instrument (guitar)
    5: fret (fret number -- 0-21, or go higher? dead notes?)
    6: string (1-6 for a standard guitar)
    7: tuning (MIDI note number that represents open string tuning)
    8: effects ('nan' or a list containing dictionaries for various effects) 
"""

def csv_to_jams(incsv, inwav, outjams):

    # Add schema for synthtab JAMS
    jams.schema.add_namespace('note_tab.json')

    # Load the audio file
    y, sr = librosa.load(inwav)

    # Compute the track duration
    track_duration = librosa.get_duration(y=y, sr=sr)

    # Construct a new JAMS object
    jam = jams.JAMS()

    # Store the track duration
    jam.file_metadata.duration = track_duration

    # Read csv file
    with open(incsv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Skip the header row
        next(reader)
        # Create variable to track the current guitar string
        string_log = 0
        # Loop through the note data
        for row in reader:
            # Create guitar string variables
            string_num = row[6]
            string_tuning = row[7]
            # Check whether a new string annotation is needed
            if string_log != string_num:
                # Add previous guitar string data to JAMS annotations 
                if string_log != 0:
                    jam.annotations.append(string_data)
                # Create a new guitar string annotation
                string_data = jams.Annotation(namespace='note_tab')
                string_data.sandbox.update(string_index=string_num, open_tuning=string_tuning) 
                # Update the string tracking variable
                string_log = string_num
            
            # Add dictionary of tablature note attributes
            value = {'fret': int(row[5]), 'velocity': int(row[3])}
            # Add any note effects to the dictionary
            if row[8] != 'nan':
                 value.update({'effects': row[8]})
            # Add an annotation for the note
            string_data.append(time=row[0], duration=row[1], value=value)

        # Add final guitar string data to JAMS annotations
        jam.annotations.append(string_data)

    jam.save(outjams)
    print(f"CSV data saved to {outjams}")
    # Add metadata to annotation (JUST USE EXAMPLE METADATA ANNOTATION FOR NOW)
    #note_tab.annotation_metadata = jams.AnnotationMetadata(data_source='human and synctoolbox')
    # POSSIBLE ISSUE - string data bundled together!!!
                
if __name__ == "__main__":

    # Create arguments to pass to csv_to_jams
    incsv = "tarrega_adelita_v2_dtw.csv"
    inwav = "Adelita_FranciscoTarrega_ArmandoFerreira.wav"
    outjams = "test-verbose.jams"
   
   # Call csv_to_jams function
    csv_to_jams(incsv, inwav, outjams)

