import urllib2
import os
import sys

usage = """
usage:
{0} http://path.to/csv output_folder
""".format(sys.argv[0])

def download_file(url, fname):
  remote = urllib2.urlopen(url)
  local = open(fname, 'wb')
  local.write(remote.read())
  local.close()

def write_metadata(data, fname):
  local = open(fname, 'w')
  local.write(data)
  local.close()

def create_metadata(fields):
  return ",".join([fields[0], fields[1]])

if len(sys.argv) != 3:
  print usage
  sys.exit(-1)

csvurl = sys.argv[1]
data_folder = os.path.abspath(sys.argv[2])

csv = urllib2.urlopen(csvurl)
for line in csv:
  fields = line.split(',')
  url = fields[2].strip()
  out_file_name = url.split("/")[-1]
  out_file_path = data_folder + '/' + out_file_name
  if not os.path.exists(data_folder):
    os.makedirs(data_folder)
  if not os.path.exists(out_file_path):
    print "downloading {0}".format(url)
    download_file(url, out_file_path)
    write_metadata(create_metadata(fields), out_file_path + '_metadata')
  else:
    print "skipping {0}".format(url)

