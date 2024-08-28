import jams
import librosa
import csv

"""
Create a function and script that converts time warped symbolic music data
in CSV format to the JAMS format.
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

    # Construct annotation record
    note_tab = jams.Annotation(namespace='note_tab')

    # Add metadata to annotation (JUST USE EXAMPLE METADATA ANNOTATION FOR NOW)
    note_tab.annotation_metadata = jams.AnnotationMetadata(data_source='human and synctoolbox')
    # POSSIBLE ISSUE - string data bundled together!!!
    # Open and read csv file
    with open(incsv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader: 
            # Dictionary of tablature note attributes
            value = {'fret': row[5], 'velocity': row[3]}
            # Add any note effects to the dictionary
            if row[8] != 'nan':
                value.update({'effects': row[8]})

            # Add an annotation for the note
            note_tab
                
if __name__ == "__main__":

    # Create arguments to pass to csv_to_jams
    incsv = "tarrega_adelita_v2_dtw.csv"
    inwav = "Adelita_FranciscoTarrega_ArmandoFerreira.wav"
    outjams = "test-verbose.jams"
   
   # Call csv_to_jams function
    csv_to_jams(incsv, inwav, outjams)

