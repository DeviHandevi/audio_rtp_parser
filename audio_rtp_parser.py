import pyshark
import sox
import os
import sys
import glob
from datetime import datetime
from operator import itemgetter
from pathlib import Path

RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
NORMAL_COLOR = '\033[0m'

LAYER_IP = 1
LAYER_RTP = 3

# Get arguments from cmd
num_of_argv = len(sys.argv)
PCAP_FILE_PARAM = '-i' # -i for pcap file name
AUDIO_FOLDER_PARAM = '-o' # -o for output folder
pcap_file_path_index = sys.argv.index(PCAP_FILE_PARAM) + 1 if PCAP_FILE_PARAM in sys.argv else num_of_argv
audio_folder_path_index = sys.argv.index(AUDIO_FOLDER_PARAM) + 1 if AUDIO_FOLDER_PARAM in sys.argv else num_of_argv
pcap_file_path = sys.argv[pcap_file_path_index] if pcap_file_path_index < num_of_argv else 0
audio_folder_path = sys.argv[audio_folder_path_index] if audio_folder_path_index < num_of_argv else 0
# If input and output params are not provided, return error
if pcap_file_path == 0 or pcap_file_path[0] == '-':
  print(RED_COLOR + 'Input PCAP file path as parameter (-i /path/to/filename.pcap)' + NORMAL_COLOR)
  raise
if audio_folder_path == 0 or audio_folder_path[0] == '-':
  print(RED_COLOR + 'Input path to audio output folder path as parameter (-o /path/to/audio_output_folder/)' + NORMAL_COLOR)
  raise

# Reading PCAP
rtp_list = []
cap = pyshark.FileCapture(pcap_file_path, display_filter='rtp')
cap.set_debug()

i = 0
filename = ''
prev_src = ''
prev_dst = ''
try:
  for c in cap:
    cur_src = c[LAYER_IP].src
    cur_dst = c[LAYER_IP].dst
    # Prepare temporary files for the raw audio (either creating a new one or append to existing)
    if cur_src != prev_src or cur_dst != prev_dst:
      filename = cur_src + '-' + cur_dst
      temp_filepath = '{}/{}.raw'.format(audio_folder_path, filename)
      raw_audio = open(temp_filepath,'ab+')
    # Get payload and write byte array to the file
    rtp = c[LAYER_RTP]
    if rtp.payload:
      rtp_list = rtp.payload.split(":")
      packet = " ".join(rtp_list)
      audio = bytearray.fromhex(packet)
      raw_audio.write(audio)
except:
  print(RED_COLOR + 'Error' + sys.exc_info()[0])
  raise
finally: 
  cap.close()

# Read from raw and write audio files
raw_filepath_list = glob.glob("{}/*.raw".format(audio_folder_path))
for raw_filepath in raw_filepath_list:
  tfm = sox.Transformer()
  tfm.set_input_format(rate=8000, channels=1, encoding='u-law')
  status = tfm.build_file(raw_filepath, '{}/{}.mp3'.format(audio_folder_path, Path(raw_filepath).stem))

print(GREEN_COLOR + 'Audio parsing finished!' + NORMAL_COLOR)
