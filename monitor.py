#!/usr/bin/env python
# coding: utf-8

import os, time, re


# ask for .bashrc alias:
has_asked_for_alias = False  # this value is changed automatically by `set_has_asked_for_alias`
bashrc_path = os.path.expanduser('~/.bashrc')

def check_alias_exists():
  if os.popen("which monitor").read().strip() != '':
    return True
  elif os.path.isfile(bashrc_path):
    with open(bashrc_path, 'r') as f:
      if 'alias monitor=' in f.read():
        return True
  return False

def set_has_asked_for_alias(has_asked=True):
  with open(__file__, 'r') as f:
    c = f.read()
  c = re.sub(r'(\s+has_asked_for_alias\s*=\s*)(?:True|False|1|0)(\s+)', r'\1%s\2' % has_asked, c, re.MULTILINE)
  with open(__file__, 'w') as f:
    f.write(c)

def set_alias():
  with open(bashrc_path, 'a+') as f:
    f.write("\nalias monitor='python \"%s\"'\n" % os.path.realpath(__file__))


# main
if __name__ == '__main__':
  if not check_alias_exists() and not has_asked_for_alias:
    resp = raw_input("Would you like to set a .bashrc alias to launch this script without typing the whole path each time? [Yes/No/Later]: ").lower().strip()
    if resp in ('y', 'yes', ''):
      set_alias()
      print("The alias was created successfully. In the next bash session you start you can simply type \"monitor\" to start this script.\n  $ monitor\n\nTo apply the alias in this session, execute the command\n  $ source ~/.bashrc\n\nStarting monitoring in 5 seconds...")
      set_has_asked_for_alias()
      time.sleep(5)
    elif resp in ('n', 'no'):
      set_has_asked_for_alias()

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
