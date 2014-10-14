import optparse
import os
import pprint
import re
import subprocess
import sys

parser = optparse.OptionParser()
parser.add_option("-i", "--input_directory", help="Directory containing folders with .avi files to transcode")

(options, args) = parser.parse_args()

# =1= Shawshank Redemption 1994 1.mkv
file_regex = re.compile('^=(.*)=\s*(.*)$')

for movie_file in os.listdir(options.input_directory):
    (movie_root, movie_ext) = os.path.splitext(movie_file)
    if movie_ext.lower() != ".mkv":
        continue
        
    match_result = file_regex.match(movie_file)
    if not match_result:
        continue
    movie_number = int(match_result.group(1))
    movie_name   = match_result.group(2)
        
    input_file = os.path.join(options.input_directory, movie_file)
    output_file = os.path.join(options.input_directory, "={0:03d}= {1}".format(movie_number, movie_name))
    
    if input_file != output_file:
        print 'move "{0}" "{1}"'.format(input_file, output_file)
