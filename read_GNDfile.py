
from cv2 import *
import numpy as np
import re

# mai radwan


def ReadGNDFile(sF):

    fid = open(sF)
    # fid = open(sF)

    sLine = next(fid)
    # % this is the number of blobs
    bGetNotes = 0
    Notes = '(none)'

    if sLine == 'GNDVERSION2.0 (INCLUDES NOTES AT THE END OF THE FILE)'.lower():
        sLine = next(fid)
        bGetNotes = 1

    NumberOfBlobEntries = re.split(sLine, '%f')
    BlobIDs = np.array[[NumberOfBlobEntries, 1]]
    for i in NumberOfBlobEntries:
        sLine = next(fid)
        # %this is the blob type...
        BlobIDs[{i}] = sLine

    sLine = next(fid)
    # % this is the number of relevant features...
    NumberOfChosenCharacteristics = re.split(sLine, '%f')
    Characteristics = np.array[[NumberOfChosenCharacteristics, 1]]
    for i in NumberOfChosenCharacteristics:
        sLine = next(fid)
        Characteristics[{i}] = sLine

    sLine = next(fid)
    NumberOfManifestations = re.split(sLine, '%f')
    sLine = next(fid)
    MaxNumberOfStates = re.split(sLine, '%f')-1

    ManifestationAndStateTypes = np.array[[NumberOfManifestations, 2]]
    for i in NumberOfManifestations:
        Manifestation = next(fid)
        # % this is the manifestation

        for j in MaxNumberOfStates:
            sLine = next(fid)
            # % this is the available state...
            if len(sLine) == 0:
                print("empty")
            elif j == 1:
                States = np.array[[1, 1]]
                States[{j, 1}] = sLine

        ManifestationAndStateTypes[{i, 1}] = Manifestation
        ManifestationAndStateTypes[{i, 2}] = States

    ActualStates = np.array[[NumberOfManifestations, 1]]
    for i in NumberOfManifestations:
        ActualStates[i] = next(fid)
    sLine = next(fid)
    # %feature
    sLine = next(fid)
    # %feature
    sLine = next(fid)
    # %feature
    sLine = next(fid)
    # %Disc-Cup ratio
    CDRatio = re.split(sLine, '%f')
    if (bGetNotes):
        Notes = next(fid)
    fid.close()

    return (BlobIDs, ManifestationAndStateTypes, ActualStates, CDRatio, Notes)
