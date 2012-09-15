import poplib
import email
import re
import os
import glob
import sys

def remove_html_tags(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def remove_extra_spaces(data):
  p = re.compile(r'\s+')
  return p.sub(' ', data)

def remove_links(data):
  p = re.compile(r'http\S+')
  return p.sub('', data)

path = sys.argv[1]

os.chdir(path)
for files in os.listdir("."):
  content = open(files, 'r').read()
  msg = email.message_from_string(content)
  if msg.is_multipart():
    payload = msg.get_payload(0)
  else:
    payload = msg.get_payload()
  if payload != None and type(payload) is str:
    content = remove_html_tags(payload)
    content = remove_extra_spaces(content)
    content = remove_links(content)
    content = remove_html_tags(content)
    print content
  s = raw_input("press 'n' for next, 's' for speak...\n\n\n")
  if s == 'n':
    continue
  elif s == 's':
    os.system("say \"{0}\"".format(content))

