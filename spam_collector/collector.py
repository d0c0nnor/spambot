import email
import glob
import os
import poplib
import re
import sys
import md5
import uuid

def remove_html_tags(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def remove_html_escapes(data):
  p = re.compile(r'&nbsp')
  return p.sub('', data)

def remove_extra_spaces(data):
  p = re.compile(r'\s+')
  return p.sub(' ', data)

def remove_links(data):
  p = re.compile(r'http\S+')
  return p.sub('', data)

def hash(data):
  return md5.new(data).hexdigest()

data = "data"

#os.chdir(path)
print "connecting"
M = poplib.POP3('pop.mailinator.com')
print "connected"
M.user('mail')
M.pass_('1234')
numMessages = len(M.list()[1])
for i in range(numMessages):
  print "retrieving message #{0}".format(i+1)
  lines = M.retr(i+1)[1]
  content = '\n'.join(lines)
  msg = email.message_from_string(content)
  if msg.is_multipart():
    payload = msg.get_payload(0)
  else:
    payload = msg.get_payload()
  if payload != None and type(payload) is str:
    content = remove_html_tags(payload)
    content = remove_html_escapes(content)
    content = remove_extra_spaces(content)
    content = remove_links(content)
    content = remove_html_tags(content)
    print content
    print "\n\n"
    print hash(content)
  raw_input("press return...")

"""
  s = raw_input("press 'n' for next, 's' for speak...\n\n\n")
  if s == 'n':
    continue
  elif s == 's':
    os.system("say \"{0}\"".format(content))
  elif s == 'y':
    uuid = uuid.uuid1()
    os.makedirs(data + '/' + uuid.hex)
    out = open(data + '/' + uuid.hex + '/message.txt')
"""