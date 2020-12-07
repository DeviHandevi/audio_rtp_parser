# Audio RTP Parser
## Project Description
This is a Audio RTP Parser project to read a PCAP file and write each audio stream to separate audio files.

## Installation
In order to run this program, there are several steps:
- Install Python 3.8 from `https://www.python.org/downloads/windows/`
- PyShark `pip install pyshark`
- Sox `pip install sox` and also install sox for windows from `http://sox.sourceforge.net/`
- Put `libmad.dll` and `libmp3lame.dll` file to sox folder from `https://app.box.com/s/tzn5ohyh90viedu3u90w2l2pmp2bl41t`

## Run
To run the parser file:
- Open cmd in the `audio_rtp_parser.py` directory
- Enter command `python audio_rtp_parser.py -i /path/to/filename.pcap -o path/to/outputfolder`
