import jams
import librosa

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

    print(jam)

if __name__ == "__main__":

    # Create arguments to pass to csv_to_jams
    incsv = "tarrega_adelita_v2_dtw.csv"
    inwav = "Adelita_FranciscoTarrega_ArmandoFerreira.wav"
    outjams = "test-verbose.jams"
   
   # Call csv_to_jams function
    csv_to_jams(incsv, inwav, outjams)

