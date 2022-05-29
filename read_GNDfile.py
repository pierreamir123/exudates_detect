
from cv2 import *
import cv2 as cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os as os
import re

# mai radwan


def ReadGNDFile(sF):

    fid = fopen(sF)
    sLine = fgetl(fid)
    # % this is the number of blobs
    bGetNotes = 0
    Notes = '(none)'

    if sLine.lower() == 'GNDVERSION2.0 (INCLUDES NOTES AT THE END OF THE FILE)'.lower():
        sLine = fgetl(fid)
        bGetNotes = 1

    NumberOfBlobEntries = re.split(sLine, '%f')
    BlobIDs = cell(NumberOfBlobEntries, 1)
    for i in NumberOfBlobEntries:
        sLine = fgetl(fid)
        # %this is the blob type...
        BlobIDs{i} = sLine

    sLine = fgetl(fid)
    # % this is the number of relevant features...
    NumberOfChosenCharacteristics = re.split(sLine, '%f')
    Characteristics = cell(NumberOfChosenCharacteristics, 1)
    for i in NumberOfChosenCharacteristics:
        sLine = fgetl(fid)
        Characteristics{i} = sLine

    sLine = fgetl(fid)
    NumberOfManifestations = re.split(sLine, '%f')
    sLine = fgetl(fid)
    MaxNumberOfStates = re.split(sLine, '%f')-1

    ManifestationAndStateTypes = cell(NumberOfManifestations, 2)
    for i in NumberOfManifestations:
        Manifestation = fgetl(fid)
        # % this is the manifestation

        for j in MaxNumberOfStates:
            sLine = fgetl(fid)
            # % this is the available state...
            if len(sLine) == 0:
                print("empty")
            elif j == 1:
                States = cell(1, 1)
                States{j, 1} = sLine

        ManifestationAndStateTypes{i, 1} = Manifestation
        ManifestationAndStateTypes{i, 2} = States

    ActualStates = cell(NumberOfManifestations, 1)
    for i in NumberOfManifestations:
        ActualStates{i} = fgetl(fid)
    sLine = fgetl(fid)
    # %feature
    sLine = fgetl(fid)
    # %feature
    sLine = fgetl(fid)
    # %feature
    sLine = fgetl(fid)
    # %Disc-Cup ratio
    CDRatio = re.split(sLine, '%f')
    if (bGetNotes):
        Notes = fgetl(fid)
    fclose(fid)

    return (BlobIDs, ManifestationAndStateTypes, ActualStates, CDRatio, Notes)
