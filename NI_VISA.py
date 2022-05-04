import datetime
import csv
import os
import pyvisa as visa
import sys
from time import sleep
import logging

logSCPI = None;
g_rm =None;
g_list_resources=None;
g_inst=None;
m_IDN =None;
def ConnectToInstrument(m_sectionname):
    global g_rm
    global g_list_resources
    global g_inst
    global logSCPI
    global m_IDN
    logSCPI = logging.getLogger()
    g_rm = visa.ResourceManager()
    #g_list_resources = g_rm.list_resources()

    g_inst = g_rm.open_resource(m_sectionname)

    send_cmd = "*IDN?"
    m_return = QueryCommand(send_cmd)
    m_IDN    = m_return
    send_cmd = "*CLS;*OPC?"
    m_return = QueryCommand(send_cmd)

def QueryCommand(sSend):
    send_cmd = sSend
    logSCPI.debug("[W]: %s" % send_cmd)
    m_return = g_inst.query(send_cmd)
    logSCPI.debug("[R]: %s" % m_return.replace('\n', '').replace('\r', ''))

    return m_return