import email
import glob
import os
import poplib
import re
import sys
import md5
import base64
import uuid
import logging
import time

usage = """
usage:
{0} output_folder
""".format(sys.argv[0])

message_file_name = 'message.txt'
topic_file_name = 'topic.txt'

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

def is_valid(data):
  return ' ' in data

def hash(data):
  return md5.new(data).hexdigest()

def cleanup(data):
  content = remove_html_tags(data)
  content = remove_html_escapes(content)
  content = remove_extra_spaces(content)
  content = remove_links(content)
  content = remove_html_tags(content)
  return content

def get_msg_payload(data):
  msg = email.message_from_string(data)
  if msg.is_multipart():
    payload = msg.get_payload(0)
  else:
    payload = msg.get_payload()
  return payload

def any_word_in_string(words, string):
  for word in words:
    if word.lower() in string.lower():
      return True
  return False

def get_topic(data):
  if any_word_in_string(['viagra', 'sex', 'penis', 'porn', 'teen', 'milf', 'tit', 'suck', 'cock', 'dick'], data):
    return 'sex'
  if any_word_in_string(['money', 'gain', '$', 'dollar', 'euro'] , data):
    return 'money'
  return 'neutral'

if len(sys.argv) != 2:
  print usage
  sys.exit(-1)

accounts = 'mail abc a aa aaa email no yes spam hi hello bye xxx x'.split(' ')
data_folder = os.path.abspath(sys.argv[1])

if __name__ == "__main__":

  while(True):
      #os.chdir(path)
    for account in accounts:

      # no need to kill the mailinator server!
      time.sleep(2)
      
      try: 
      
        print "connecting to account {0}".format(account)
        M = poplib.POP3('pop.mailinator.com')
        print "connected"
        M.user(account)
        M.pass_('1234')
        numMessages = len(M.list()[1])
        for i in range(numMessages):
          print "retrieving message #{0}".format(i+1)
          lines = M.retr(i+1)[1]
          content = '\n'.join(lines)
          payload = get_msg_payload(content)
          if payload != None and type(payload) is str:
            content = cleanup(payload)
            if content.count(' ') == 0:
              content = base64.b64decode(content)
              content = get_msg_payload(content)
              content = cleanup(content)
            if content.count(' ') == 0:
              continue

            content_white_spaces = content.count(' ')
            content_len = len(content)
            ratio = float(content_white_spaces) / content_len
            if ratio < 0.1:
              continue
            if len(content) > 1000:
              continue

            content_hash = hash(content)
            destination_folder = data_folder + '/' + content_hash
            destination_file = destination_folder + '/' + message_file_name
            destination_topic_file = destination_folder + '/' + topic_file_name
            if not os.path.exists(destination_folder):
              print "saving {0}".format(content_hash)
              print content
              print "ratio: {0}/{1}={2}".format(content_white_spaces, content_len, ratio)
              os.makedirs(destination_folder)
              f = open(destination_file, 'w')
              f.write(content)
              f.close()
              f = open(destination_topic_file, 'w')
              f.write(get_topic(content))
              f.close()

      except Exception, e:
        logging.exception("Couldn't retrieve mail", e)

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
