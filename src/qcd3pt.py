import numpy as np
import h5py
import pathlib
import re

numberRegex = re.compile(r'-?\d+')

def text_number_regex(startText):
    return re.compile(startText+r'-?\d+(?:[_.]|\Z)') # regular expression to find t value

def extract_number(regex, text):
    # extract ti value
    match = regex.search(text)
    if match is None:
        print("ERROR: Regex", regex, "couldn't find value in %s" % text)

    numberMatch = numberRegex.findall(match.group())
    return int(numberMatch[0])

def load_mean_data(rawFilename, arrFilename, forceGenerate=False):
    ## load saved np array and return if it exists
    arrPath = pathlib.Path(arrFilename)
    if not forceGenerate:
        if arrPath.is_file():
            with open(arrPath, 'rb') as arrFile:
                return np.load(arrFile)

    ## mean over lattices of each configuration
    # open h5 file
    rawFile = h5py.File(rawFilename, 'r')
    stream = rawFile['stream_a']
    confs_list = []

    # extract data
    # regular expressions for extracting numbers
    tRegex = text_number_regex('t')
    rStrings = ('x', 'y', 'z')
    rRegex = tuple(text_number_regex(startString) for startString in rStrings)
    pStrings = ('px', 'py', 'pz')
    pRegex = tuple(text_number_regex(startString) for startString in pStrings)
    nDims = 3
    
    for j, conf in zip(range(len(stream.values())), stream.values()):
        lattices = []
        for i, item in zip(range(len(conf.items())), conf.items()):
            #convert to complex array
            latticeFloat = np.array(item[1]).squeeze()
            latticeComplexShape = latticeFloat.shape
            latticeComplexShape = (*latticeComplexShape[:-1], latticeComplexShape[-1]//2)

            #latticeComplex = np.empty(len(latticeFloat)//2, np.cdouble)
            latticeComplex = np.empty(latticeComplexShape, np.cdouble)
            latticeComplex.real = latticeFloat[:, :, 0::2]
            latticeComplex.imag = latticeFloat[:, :, 1::2]

            # corrections based on position in space, momentum and time
            name = item[0]
            ti = extract_number(tRegex, name)
            r = np.array(tuple(extract_number(regex, name) for regex in rRegex))
            p = np.array(tuple(extract_number(regex, rawFilename) for regex in pRegex))
            q = np.zeros(nDims) # TODO: extract this from rawFilename

            ## roll initial time (ti) to 0
            latticeComplex = np.roll(latticeComplex, -ti, 2)
            ## add phase from fourier transform
            phaseFactor = np.exp(-1j * ((p+q) @ r))
            latticeComplex = latticeComplex * phaseFactor
            lattices.append(latticeComplex)

            ##TODO: work with the different values for different 4-indices
            #if i == 0 and j == 0:
            #    print(ti)

        confs_list.append(np.mean(np.array(lattices), 0))

    confs = np.array(confs_list)

    # save np array
    with open(arrPath, 'wb') as arrFile:
        np.save(arrFile, confs)

    return confs
