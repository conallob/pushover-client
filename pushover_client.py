#!/usr/local/bin/python2.7
# vim:ts=2:sw=2:expandtab:ft=python:fileencoding=utf-8

# $Id$

# Copyright (c) 2012, Conall O'Brien
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Conall O'Brien ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


__author__ = "Conall O'Brien (conall@conall.net)"


__version__ = 0.1

import gflags as flags
import requests
import sys

flags.DEFINE_string("user", None, "Pushover.net UserID", short_name="U")
flags.DEFINE_string("token", None, "Pushover.net Token", short_name="Z")
flags.DEFINE_string("title", None, "Message Title", short_name="T")
flags.DEFINE_string("device", None, "Target Device. Default: All",
                    short_name="D")
flags.DEFINE_string("message", None, "Message Body", short_name="M")
flags.DEFINE_bool("important", False, "Priotiy bit", short_name="I")
flags.DEFINE_bool("stdin", False, "Read from stdin instead of --message")
flags.DEFINE_bool("verbose", False, "Increase verbosity", short_name="V")
# Required flags
flags.MarkFlagAsRequired("user")
flags.MarkFlagAsRequired("token")


FLAGS = flags.FLAGS


HEADERS = {
  "useragent": "pushover_client/%.1f" % __version__ ,
  }

class FlagsError(Exception):
  pass


def _GenerateMessageObject(msg):
  data = {
    "token": FLAGS.token,
    "user": FLAGS.user,
    "title": FLAGS.title,
    "priority": int(FLAGS.important),
    "message": msg,
  }
  if FLAGS.device is not None:
    data["device"] = FLAGS.device
  return data


def app():
  argv = FLAGS(sys.argv)
  if FLAGS.stdin and FLAGS.message:
    raise FlagsError("--message and --stdin flags cannot be used together")
  if FLAGS.stdin:
    try:
      msg = sys.stdin.readlines()
    except:
      raise InputError("Unable to read stdin")
  else:
    msg = FLAGS.message
  data = _GenerateMessageObject(msg)
  if FLAGS.verbose:
    print data
  # TODO(conall): Add some error handling here
  api = requests.post("https://api.pushover.net/1/messages",
                      headers=HEADERS, data=data)
  if FLAGS.verbose:
    print api.status_code


if __name__ == "__main__":
  app()
