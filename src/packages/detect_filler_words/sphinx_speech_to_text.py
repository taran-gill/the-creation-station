from __future__ import division
from pocketsphinx.pocketsphinx import *
from os import environ, path, listdir
import sys
import time
import wave
from analyze_filler_words import *

# directory paths
MODELDIR = "/sphinx/pocketsphinx/model"
DATADIR = "./src/packages/detect_filler_words/data" #wav files
HYPDIR = "./src/packages/detect_filler_words/data/hyp_test" # stores test hypotheses

# paths to dictionaries
hmmd = '/sphinx/pocketsphinx/en-us/en-us'
lmd = '/sphinx/pocketsphinx/en-us/en-us.lm.bin'
dictd = '/sphinx/pocketsphinx/en-us/cmudict-en-us.dict'

# create a decoder
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

def write_hypothesis(outfile, segments):
    ''' Writes the hypothesis file'''
    with open(path.join(HYPDIR, outfile), 'w') as o:
        for word in segments:       
            o.write(word+' ')  
    o.close()  
    
def decode(datadir, filename):
    ''' Decode streaming data.'''
    decoder = Decoder(config)
    decoder.start_utt()
    
    stream = open(path.join(datadir,filename),'rb')
    
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()
    segments = [seg.word for seg in decoder.seg()]
    f = 'hypothesis-'+filename.split('.')[0]+'.txt'
    print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
    write_hypothesis(f, segments)
    return segments

def file_in_correct_format(filename):
    ''' Checks if the provided file is in the correct format 
        (i.e. mono channel with a sampling rate of 16000).
        returns True if it is in the correct format and False 
        if it isn't. Also prints out an error message if the 
        file is not in the correct format
    '''
    wf = wave.open(filename, 'rb')
    # get information about the audio file provided
    channels = wf.getnchannels()
    rate = wf.getframerate()
    
    # print error message if the format of provided file is incorrect
    if not channels == 1 or not rate == 16000:
        print ('ERROR: file provided is not in the correct format. Please provide a mono channel file with a sampling rate of 16000')
        return False
    return True
        
if __name__=='__main__':
    global filename
    start = time.time()

    # if len(sys.argv)== 2:
    # if one argument provided, it's a filename 
    # and assume the data directory is the default data directory
    #filename = sys.argv[1]
    filename = "uhm.wav"
    if file_in_correct_format(path.join(DATADIR, filename)):
        segments = decode(DATADIR, filename)
        new_list = preprocess_segments(segments)
        print ('\n************* RESULTS ****************')
        filler_words(new_list)
        
    # elif len(sys.argv)==3:
    #     # if two arguments provided, the first argument will be the data directory and the second the filename
    #     datadir = sys.argv[1]
    #     filename = sys.argv[2]
        
    #     if file_in_correct_format(path.join(datadir, filename)):
    #         segments = decode(datadir, filename)
    #         new_list = preprocess_segments(segments)
    #         print ('\n************* RESULTS ****************')
    #         filler_words(new_list)
    # else:
    #     # if no args provided, run the decoder on all files in the default DATADIR
    #     # this assumes there are only .wav files in the directory (not including
    #     # other directories. throws an error if 
    #     for f in listdir(DATADIR):
    #         if not f.startswith('.') and path.isfile(path.join(DATADIR, f)):
    #             if file_in_correct_format(path.join(DATADIR, f)):
    #                 decode(DATADIR, f)
    end = time.time()
    print ('time elapsed:' +  str(end - start))
