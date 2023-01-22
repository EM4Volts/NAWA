from __future__ import annotations
from functools import wraps
import json
import os
from time import time
from typing import Dict, List

def to_int(bs):
    return (int.from_bytes(bs, byteorder='little'))

class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = [x, y, z]



def getObjKey(obj):
    p1 = obj.name.split('-')
    if p1[0].isdigit():
        return f"{int(p1[0]):04d}-"
    else:
        return f"0000-{obj.name}"

def create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def print_class(obj):
    return


def volumeInsideOther(volumeCenter, volumeScale, otherVolumeCenter, otherVolumeScale):
    xVals = [volumeCenter[0] - volumeScale[0]/2, volumeCenter[0] + volumeScale[0]/2]
    yVals = [volumeCenter[1] - volumeScale[1]/2, volumeCenter[1] + volumeScale[1]/2]
    zVals = [volumeCenter[2] - volumeScale[2]/2, volumeCenter[2] + volumeScale[2]/2]

    other_xVals = [otherVolumeCenter[0] - otherVolumeScale[0]/2, otherVolumeCenter[0] + otherVolumeScale[0]/2]
    other_yVals = [otherVolumeCenter[1] - otherVolumeScale[1]/2, otherVolumeCenter[1] + otherVolumeScale[1]/2]
    other_zVals = [otherVolumeCenter[2] - otherVolumeScale[2]/2, otherVolumeCenter[2] + otherVolumeScale[2]/2]

    if (max(xVals) <= max(other_xVals) and max(yVals) <= max(other_yVals) and max(zVals) <= max(other_zVals)):
        if (min(xVals) >= min(other_xVals) and min(yVals) >= min(other_yVals) and min(zVals) >= min(other_zVals)):
            return True
    return False


def getVolumeSurrounding(volumeCenter, volumeScale, otherVolumeCenter, otherVolumeScale):
    xVals = [volumeCenter[0] - volumeScale[0]/2, volumeCenter[0] + volumeScale[0]/2, otherVolumeCenter[0] - otherVolumeScale[0]/2, otherVolumeCenter[0] + otherVolumeScale[0]/2]
    yVals = [volumeCenter[1] - volumeScale[1]/2, volumeCenter[1] + volumeScale[1]/2, otherVolumeCenter[1] - otherVolumeScale[1]/2, otherVolumeCenter[1] + otherVolumeScale[1]/2]
    zVals = [volumeCenter[2] - volumeScale[2]/2, volumeCenter[2] + volumeScale[2]/2, otherVolumeCenter[2] - otherVolumeScale[2]/2, otherVolumeCenter[2] + otherVolumeScale[2]/2]

    minX = min(xVals)
    maxX = max(xVals)
    minY = min(yVals)
    maxY = max(yVals)
    minZ = min(zVals)
    maxZ = max(zVals)

    midPoint = [(minX + maxX)/2, (minY + maxY)/2, (minZ + maxZ)/2]
    scale = [maxX - midPoint[0], maxY - midPoint[1], maxZ - midPoint[2]]
    return midPoint, scale

def setTiming(path: List[str], time: float, inner: Dict|None = None):
    if inner is None:
        inner = timings
    if len(path) == 1 and type(inner.get(path[0])) is dict:
        path.append("_TOTAL")
    if len(path) == 1:
        if path[0] not in inner:
            inner[path[0]] = 0
        inner[path[0]] += time
    else:
        if path[0] not in inner:
            inner[path[0]] = {}
        setTiming(path[1:], time, inner[path[0]])

def resetTimings():
    global timings, startTime
    timings = {}
    startTime = time()

def timing(path: List[str]):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kw):
            # t1 = time()
            result = f(*args, **kw)
            # t2 = time()
            # setTiming(path, t2 - t1)
            return result
        return wrap
    return decorator

def printTimingsSection(total: float, inner: Dict, indent: int = 0):
    for key in inner:
        if type(inner[key]) is dict:
            return
        else:
            return

def printTimings():
    print("Timings:")
    print(json.dumps(timings, indent=4))
    total = time() - startTime
    print("Total: " + str(total))
    printTimingsSection(total, timings)


def getFileSortingKey(file: str):
    base, ext = os.path.splitext(file)
    return (base.lower(), ext.lower())



def saveDatInfo(filepath: str, files: List[str], filename: str):
    files = list(set(files))
    files.sort(key=getFileSortingKey)
    base, ext = os.path.splitext(filename)
    with open(filepath, 'w') as f:
        jsonFiles = {
            "version": 1,
            "files": files,
            "basename": base,
            "ext": ext[1:]
        }
        json.dump(jsonFiles, f, indent=4)
