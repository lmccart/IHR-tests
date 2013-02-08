#!/usr/bin/python2.4

'''Post a message to twitter'''


import ConfigParser
import getopt
import os
import sys
import twitter
import pika

class TweetRc(object):
  def __init__(self):
    self._config = None

  def GetConsumerKey(self):
    return self._GetOption('consumer_key')

  def GetConsumerSecret(self):
    return self._GetOption('consumer_secret')

  def GetAccessKey(self):
    return self._GetOption('access_key')

  def GetAccessSecret(self):
    return self._GetOption('access_secret')

  def _GetOption(self, option):
    try:
      return self._GetConfig().get('Tweet', option)
    except:
      return None

  def _GetConfig(self):
    if not self._config:
      self._config = ConfigParser.ConfigParser()
      self._config.read(os.path.expanduser('.tweetrc'))
    return self._config

def main():

  # twitter
  message = 'test1'
  rc = TweetRc()
  consumer_key = rc.GetConsumerKey()
  consumer_secret = rc.GetConsumerSecret()
  access_key = rc.GetAccessKey()
  access_secret = rc.GetAccessSecret()
  if not consumer_key or not consumer_secret or not access_key or not access_secret:
    print 'no info'
  api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token_key=access_key, access_token_secret=access_secret)
#   try:
#     status = api.PostUpdate(message)
#   except UnicodeDecodeError:
#     print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
#     print "Try explicitly specifying the encoding with the --encoding flag"
#     sys.exit(2)
#   print "%s just posted: %s" % (status.user.name, status.text)
  
  #RabbitMQ
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.queue_declare(queue='hello')
  channel.basic_publish(exchange='', routing_key='hello', body='hello world.')
  print " [x] Sent 'hello world.'"
  connection.close()

if __name__ == "__main__":
  main()
  
