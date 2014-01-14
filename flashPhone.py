__author__ = 'jiahuixing'
# -*- coding: utf-8 -*-

import urllib
import socket
import re
from commonLib import *


def flash_phone():
    """


    """
    version = get_date()
    socket.setdefaulttimeout(TIMEOUT)
    try:
        web = urllib.urlopen(INNER_MAIN_PAGE).read()
        if version in web:
            debug('Find version.')
            judge_input(CHOOSE_T_SYS)
            num = get_num_value()
            debug('num=%s' % num)
            if num:
                page = INNER_MAIN_PAGE + version
                web = urllib.urlopen(page).readlines()
                for line in web:
                    if '.tar' in line:
                        tar = find_tar(num, line)
                        if tar:
                            debug('tar=%s' % tar)
                            url = INNER_MAIN_PAGE + version + '/' + tar
                            debug('url=%s' % url)
                            if not os.path.exists(tar):
                                to_download_file(url)
                            else:
                                debug('tar exists')
                            run_script(tar)
                            break
        else:
            debug('Did not find this version.')
    except IOError, err1:
        debug(err1)
        debug('Inner web is down.Try to get file from outer.')
        file_name = str(raw_input('Pls input filename:\n').strip('\r').strip('n'))
        try:
            url = OUTER_MAIN_PAGE + version + '/' + file_name
            web = urllib.urlopen(url).code
            if web == 200:
                to_download_file(url)
            else:
                debug('url=%s' % url)
                debug('Did not find this file.')
        except IOError, err2:
            debug(err2)
            debug('Did not find this file.')


def find_tar(num, line):
    """

    :param num:
    :param line:
    :return:
    """
    choose = CHOOSE[num - 1]
    version = get_date()
    tar_name = choose + MIDDLE + version + IMAGES_SUF
    #    debug('tar_name=%s'%tar_name)
    pat = re.compile(tar_name)
    result = re.search(pat, line)
    if result:
        debug('Find it')
        tar = result.group()
    else:
        #debug('cant find it')
        tar = ''
    return tar


def judge_input(choose_type=CHOOSE_T_IN):
    """

    :param choose_type:
    """
    debug(choose_type)
    try:
        if len(CHOOSE) > 9:
            read_len = 2
        else:
            read_len = 1
        if len(sys.argv) > 2 and choose_type == CHOOSE_T_SYS:
            m_input = sys.argv[2][:read_len]
            set_num_value(m_input)
        else:
            info = 'Pls choose the num to down the tar:\n'
            info = get_info(info, CHOOSE)
            debug(info)
            m_input = sys.stdin.read(read_len)
            if m_input.isdigit():
                m_input = int(m_input)
                if m_input in range(1, len(CHOOSE) + 1):
                    debug('m_input=%s' % m_input)
                    set_num_value(m_input)
                else:
                    debug('Pls input num in %s--%s.' % (1, len(CHOOSE)))
                    judge_input()
            else:
                debug('Not a valid num,pls re input')
                judge_input()
    except KeyboardInterrupt:
        debug('Interrupt')


def to_download_file(url):
    """

    :param url:
    """
    down = DOWNLOAD_COMMAND + url
    debug('down=%s' % down)
    run_command(down)


def run_script(tar):
    """

    :param tar:
    """
    flash = FLASH_SCRIPT + tar
    debug('flash=%s' % flash)
    run_command(flash)


flash_phone()
