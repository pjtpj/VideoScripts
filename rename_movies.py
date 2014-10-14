import optparse
import os
import pprint
import re
import subprocess
import sys

parser = optparse.OptionParser()
parser.add_option("-i", "--input_directory", help="Directory containing folders with .avi files to transcode")
parser.add_option("-o", "--output_directory", help="Directory to hold output .mkv files")
parser.add_option("-b", "--begin_number", help="Number of first directory to process", default=1, type="int")
parser.add_option("-e", "--end_number", help="Number of last directory to process", default=999, type="int")
parser.add_option("-x", action="store_true", default=False, help="Execute commands", dest="execute")

(options, args) = parser.parse_args()

def execute(command):
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise Exception("Process error {0} on command '{1}': {2}".format(exitCode,  command, output))

# =243= Kill Bill Volume 2 2004
folder_regex = re.compile('^=(.*)=\s*(.*)$')
srt_extensions = ['.srt', '.sub', '.txt']

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
    # print "movie_name: {0} movie_number: {1}".format(movie_name, movie_number)

    movie_file_count = 0
    for movie_file in os.listdir(movie_folder):
        (movie_root, movie_ext) = os.path.splitext(movie_file)
        if movie_ext.lower() != ".avi":
            continue

        movie_file_count += 1

        input_file = os.path.join(options.output_directory, "{0} {1}.mkv".format(movie_name, movie_file_count))
        output_file = os.path.join(options.output_directory, "={0}= {1} {2}.mkv".format(movie_number, movie_name, movie_file_count))
        
        print 'move "{0}" "{1}"'.format(input_file, output_file)
