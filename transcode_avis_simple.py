import optparse
import os
import pprint
import re
import subprocess
import sys

parser = optparse.OptionParser()
parser.add_option("-i", "--input_directory", help="Directory containing folders with .avi files to transcode")
parser.add_option("-o", "--output_directory", help="Directory to hold output .mkv files")
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

for movie_file in os.listdir(options.input_directory):
	(movie_root, movie_ext) = os.path.splitext(movie_file)
	if movie_ext.lower() != ".avi":
		continue
		
	input_file = os.path.join(options.input_directory, movie_file)
	output_file = os.path.join(options.output_directory, movie_root + ".mkv")

	# HandBrakeCLI -i Pulp.Fiction.cd1.DVDRip.XViD.AC3.iNTERNAL-FFM.avi --srt-file Pulp.Fiction.cd1.DVDRip.XViD.AC3.iNTERNAL-FFM.srt -o Pulp\ Fiction\ [1994]-cd1.mkv -e x264 -q 22 -E copy
	if options.execute:
		transcode_command = ['HandBrakeCLI', '-i', input_file, '-o', output_file, '-e', 'x264', '-q', '22', '-E', 'copy']
		execute(transcode_command)
	else:
		transcode_command = 'HandBrakeCLI -i "{0}" -o "{1}" -e x264 -q 22 -E copy'.format(input_file, output_file)
		print transcode_command
