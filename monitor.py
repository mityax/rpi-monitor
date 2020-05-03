#!/usr/bin/env python
# coding: utf-8

import os, time, re

av = ([], [], [])
color_codes = ('\33[31m', '\33[33m', '\033[33m')

while True:
  dat = []
  dat.append(os.popen("vcgencmd measure_temp").read().replace("'", "°"))

  v = 0
  for id in ('core', 'sdram_c', 'sdram_i', 'sdram_p'):
    v += float(os.popen("vcgencmd measure_volts %s" % id).read().strip()[5:-1])
  dat.append('core=%sV' % os.popen("vcgencmd measure_volts core").read().strip()[5:-1])
  dat.append('volt=%sV' % v)

  current_round = av[0][1] if av[0] else 0
  s = "%s%d:\t" % (' '*(3-len(str(current_round))), current_round)

  for i, el in enumerate(dat):
    num_match = re.match(r'.*?((\d+(?:\.\d+)?).*?)$', el)
    num = float(num_match.group(2))
    if av[i]:
      av[i][0] = (av[i][0] * av[i][1] + num) / (av[i][1] + 1)
      av[i][1] = av[i][1] + 1
    else:
      av[i].extend([num, 1])
    el = el.replace(num_match.group(1), '\33[1m%s%s\33[0m' % (color_codes[i], num_match.group(1)))
    s += "%s av=\33[1m%s\33[0m\t" % (el.strip(), round(av[i][0], 2))

  print(s)

  time.sleep(1)
