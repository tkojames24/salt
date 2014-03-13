# -*- coding: utf-8 -*-
'''
Salt Key makes use of the outputter system to format information sent to the
``salt-key`` command. This outputter is geared towards ingesting very specific
data and should only be used with the salt-key command.
'''

# Import salt libs
import salt.utils


def output(data):
    '''
    Read in the dict structure generated by the salt key API methods and
    print the structure.
    '''
    color = salt.utils.get_colors(__opts__.get('color'))
    if __opts__['transport'] == 'zeromq':
        acc = 'minions'
        pend = 'minions_pre'
        rej = 'minions_rejected'
    else:
        acc = 'accepted'
        pend = 'pending'
        rej = 'rejected'

    cmap = {pend: color['RED'],
            acc: color['GREEN'],
            rej: color['BLUE'],
            'local': color['PURPLE']}

    trans = {pend: '{0}Unaccepted Keys:{1}'.format(
                                color['LIGHT_RED'],
                                color['ENDC']),
             acc: '{0}Accepted Keys:{1}'.format(
                                color['LIGHT_GREEN'],
                                color['ENDC']),
             rej: '{0}Rejected Keys:{1}'.format(
                                color['LIGHT_BLUE'],
                                color['ENDC']),
             'local': '{0}Local Keys:{1}'.format(
                                color['LIGHT_PURPLE'],
                                color['ENDC'])}

    ret = ''

    for status in sorted(data):
        ret += '{0}\n'.format(trans[status])
        for key in data[status]:
            if isinstance(data[status], list):
                ret += '{0}{1}{2}\n'.format(
                        cmap[status],
                        key,
                        color['ENDC'])
            if isinstance(data[status], dict):
                ret += '{0}{1}:  {2}{3}\n'.format(
                        cmap[status],
                        key,
                        data[status][key],
                        color['ENDC'])
    return ret
