import pyshark
import sox
import os
import sys
from datetime import datetime

RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
NORMAL_COLOR = '\033[0m'

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
elif audio_folder_path == 0 or audio_folder_path[0] == '-':
  print(RED_COLOR + 'Input path to audio output folder path as parameter (-o /path/to/audio_output_folder/)' + NORMAL_COLOR)
else:
  # Reading PCAP
  rtp_list = []
  cap = pyshark.FileCapture(pcap_file_path, display_filter='rtp')
  cap.set_debug()

  try:
    for c in cap:
      rtp = c[3]
      if rtp.payload:
        rtp_list.append(rtp.payload.split(":"))
  except:
    pass
  finally: 
    cap.close()

  # Prepare temporaty files for the raw audio
  timestamp = datetime.timestamp(datetime.now())
  temp_filepath = '{}/{}.raw'.format(audio_folder_path, timestamp)
  raw_audio = open(temp_filepath,'wb')
  for rtp_packet in rtp_list:
    packet = " ".join(rtp_packet)
    audio = bytearray.fromhex(packet)
    raw_audio.write(audio)


  # Read from raw and write audio files
  tfm = sox.Transformer()
  tfm.set_input_format(rate=8000, channels=1, encoding='u-law')
  status = tfm.build_file(temp_filepath, '{}/{}.mp3'.format(audio_folder_path, timestamp))

  print(GREEN_COLOR + 'Audio parsing finished!' + NORMAL_COLOR)

  # python audio_rtp_parser.py -i D:/Downloads/coba_proses7.pcap -o D:/Downloads/output