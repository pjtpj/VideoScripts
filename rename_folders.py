import optparse
import os
import pprint
import re

parser = optparse.OptionParser()
parser.add_option("-i", "--input_directory", help="Directory containing folders with .avi files to transcode")
parser.add_option("-b", "--begin_number", help="Number of first directory to process", default=1, type="int")
parser.add_option("-e", "--end_number", help="Number of last directory to process", default=999, type="int")

(options, args) = parser.parse_args()

# -=99=-Princess Mononoke
folder_regex = re.compile('^-=(.*)=-{0,1}(.*)$')
movie_strip_patterns = [
    '\s*DVDRip\s*',
    '\s*XviD-GuYoZ\s*',
    '\s*XViD-ALLiANCE\s*',
    '\s*Xvid\s*AC3-FLAWL3SS\s*',
    '\s*iNTERNALXviD-UNDEAD\s*',
    '\s*XViD\s*AC3\s*iNTERNAL-FFM\s*',
    '\s*DVDRiP\s*XviD-aXXo\s*',
    '\s*PROPERXViD-VH-PROD\s*',
    '\s*DvDrip-aXXo\s*',
    '\s*DVDrip\s*DivX-DiAMOND\s*',
    '\s*AC3 INTERNAL dvdrip xvid-saphire\s*',
    '\s*\-DVDRIP\s*',
    '\s*REAL PROPER\s*',
    '\s*REMASTERED\s+1942.*',
    '\s*DVD.*ARROW\s*',
    '\s*INTERNAL-GZP\s*',
    '\s*iNTERNAL-CULT\s*',
    '\s*iNTERNAL-iNCiTE\s*',
    '\s*iNTERNAL AC3XViD-W4E\s*',
    '\s*DvDRip XViD-sFZ\s*',
    '\s*AC.*OND\s*',
    '\s*LIMITEDDivX-HOSTiLE\s*',
    '\s*INT.*aLe\s*',
    '\s*AC3 XViDVD iNT-xCZ\s*',
    '\s*DvDivX-INTERNAL-BLooDWeiSeR\s*',
    '\s*XVID DvDRip-NoGrp\s*',
    '\s*LIMITEDDivX-ViTE\s*',
    '\s*CE INTERNAL\s*',
    '\s*Limited READ NFODivX-DVL\s*',
    '\s*MultiSub-CiN\s*',
    '\s*WS.*ENT\s*',
    '\s*INTERNAL DVDRiP DiVX-MDX\s*',
    '\s*XVID AC3 EN\s*',
    '\s*DvDrip.*FXG\s*',
    '\s*\-PUKKA\s*',
    '\s*INTERNAL-RTT\s*',
    '\s*\-VoMiT\s*',
    '\s*INTE.*ZO\s*',
    '\s*DVDRiP XViD-MRUSH\s*',
    '\s*DVDrip XViD-DVL\s*',
    '\s*iNT-ApReCiAte\s*',
    '\s*\-LOL\s*',
    '\s*INTERNAL AC3-RETRO\s*',
    '\s*DVDRiP XViD-mVs\s*',
    '\s*DVDRIP XVID iNT-iGNiTE\s*',
    '\s*DvDrip\[Eng\]\-FXG\s*',
    '\s*EXT.*aLe\s*',
    '\s*DVDrip-RARE\s*',
    '\s*XViD AC3\s*',
    '\s*\-Divx ChAoS-NeT\s*',
    '\s*Dvdrip Xvid AC3\[5 1\]CK\s*',
    '\s*REMAST.*N\s*',
    '\s*\-RETRO\s*',
    '\s*EXT.*CO\s*',
    '\s*ws-pdtv xvid\s*',
    '\s*480p.*3SS\s*',
    '\s*\(xvid110\-sickboy88\)\s*',
    '\s*\.LiM.*LPD\s*',
    '\s*XViD\-CFH\s*',
    '\s*WSXViD iNT-EwDp\s*',
    '\s*RIp XVid - THC\s*',
    '\s*\.1\-FLAWL3SS\s*',
    '\s*rip Xvid\s*',
    '\s*RE.*DASH\s*',
    '\s*iNTERNAL\s*',
    '\s*KLAXXON\s*',
    '\s*\-iNCiTE\s*',
    '\s*\-CULT\s*',
    '\s*XviD\s*',
    '^\s+',
    '\s+$',
    '\s*\[\]\s*',
    '\s*\[Ac3\]\s*',
    '\s*\[Eng\]\s*',
    '\s*\[DVDrip\]\s*',
    '\s*\-XVID\s*',
    '\s*XVID\s*',
    '\s*AC3\s*',
    '\s*DvDrip\s*',
    '\s*\-*aXXo\s*',
    '\s*DVDRiP\s*',
    '\s*\-*DVD(-R)*\s*',
    '\s*REMASTERED SE-iMOVANE\s*',
    '\s*INTERNAL\s*',
    '\s*\-*RARE\s*',
    '\s*\-*RoSub\s*',
    '\s*\-*RoSub\s*',
    '\s*\-*DoNE\s*',
    '\s*REMASTERED\s*',
    '\s*RECUT\s*',
    '\s*EXTENDED\s*',
    '\s*\-*EPiC\s*',
    '\s*\.*BRRip\.*\s*',
    '\s*\-DiAMOND\s*',
    '\s*RETAIL\s*',
    '\s*XViD(\-XV)*\s*',
    '\s*rip-FXG\s*',
    '\s*DivX\s*',
    '\s*DEiTY\s*',
]

for file_name in os.listdir(options.input_directory):
    movie_folder = os.path.join(options.input_directory, file_name)
    if not os.path.isdir(movie_folder):
        continue
    # print "file_name: {0}".format(file_name)

    match_result = folder_regex.match(file_name)
    if not match_result:
        continue
    movie_number = int(match_result.group(1))
    movie_name   = match_result.group(2)
    if (movie_number < options.begin_number or movie_number > options.end_number):
        continue
    # Strip out annoying words from movie names
    for pattern in movie_strip_patterns:
        movie_name = re.sub(pattern, '', movie_name)
    movie_name = "={0:03d}= {1}".format(movie_number, movie_name)

    print "Rename '{0}' to '{1}'".format(file_name, movie_name)
    os.rename(movie_folder, os.path.join(options.input_directory, movie_name))
