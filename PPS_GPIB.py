# This is a sample Python script.
import datetime
import csv
import os
import sys
from time import sleep
import NI_VISA as m_visa
import logging

log = None;
Version = '1.00.004'
Built_Date = "2022/05/05"


if __name__ == '__main__':
    FORMAT = '[%(asctime)s][%(levelname)s][%(name)s] %(message)s'
    logging.basicConfig(filename='Debug.log', level=logging.DEBUG, encoding='utf-8', format=FORMAT,filemode='w')
    log = logging

    log.info('Logger %s Start!' % log.getLogger())


    bIsParmDone = False
    bIsHelp = False
    if len(sys.argv) == 1:
        bIsHelp = True
        bIsParmDone = False
    elif len(sys.argv) == 2:
        if ((sys.argv[1].find("-v") != -1) or (sys.argv[1].find("-version") != -1)):
            print("Version: %s Built_Date: %s" % (Version,Built_Date))
        elif sys.argv[1].find("?") != -1 or sys.argv[1].find("-help") != -1  or sys.argv[1].find("-h") != -1:
            bIsHelp = True
            bIsParmDone = False
    else:
        if len(sys.argv) > 2:
            mode = sys.argv[1]
            saddress = sys.argv[2]
            soutput = sys.argv[3]
            bIsParmDone = True
            if mode == 'ON':
                if len(sys.argv) > 5:
                    svolt = sys.argv[4]
                    scurr = sys.argv[5]
                    bIsParmDone = True
                else:
                    bIsParmDone = False
                    bIsHelp = True
            elif mode == 'MEAS':
                if len(sys.argv) > 6:
                    IsOnOff = sys.argv[4]
                    Timeout = sys.argv[5]
                    meas_delay = sys.argv[6]
                    bIsParmDone = True
                else:
                    bIsParmDone = False
                    bIsHelp = True
        else:
            bIsParmDone = False
            bIsHelp = True


    if bIsParmDone:
        sectionname = "GPIB0::%s::INSTR" % saddress
        #sectionname = 'TCPIP0::192.168.1.11::INST0::INSTR'
        m_visa.ConnectToInstrument(sectionname)
        log.info('IDN = %s' % m_visa.m_IDN.replace('\n', '').replace('\r', ''))

        send_cmd = "INST:SEL OUT%s;*OPC?" % soutput
        m_return = m_visa.QueryCommand(send_cmd)

        send_cmd = "INST:SEL?"
        m_return = m_visa.QueryCommand(send_cmd)

        if mode == 'ON':
            send_cmd = "VOLT %s;*OPC?" % svolt
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "CURR %s;*OPC?" % scurr
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "VOLT?"
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "CURR?"
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "OUTPut %s;*OPC?" % mode
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "OUTPut?"
            m_return = m_visa.QueryCommand(send_cmd)

        elif mode == 'OFF':
            send_cmd = "OUTPut %s;*OPC?" % mode
            m_return = m_visa.QueryCommand(send_cmd)

            send_cmd = "OUTPut?"
            m_return = m_visa.QueryCommand(send_cmd)

        elif mode == 'MEAS':

            if IsOnOff == 'YES':
                send_cmd = "OUTPut %s;*OPC?" % 'OFF'
                m_return = m_visa.QueryCommand(send_cmd)

                send_cmd = "OUTPut %s;*OPC?" % 'ON'
                m_return = m_visa.QueryCommand(send_cmd)

            csvfilename = 'power_data.csv'
            if os.path.isfile(csvfilename):
                os.remove(csvfilename)

            with open(csvfilename, 'w', newline='') as csv_log:
                writer = csv.writer(csv_log)
                i = 0
                looptimeout = float(Timeout)
                sleeptimems = float(meas_delay)
                start_time = datetime.datetime.now()
                writer.writerow(["NO", "TIME_MS", "V", "A", "W"])
                execution_time = 0.0
                while execution_time < looptimeout:
                    Delay = sleeptimems / 1000
                    send_cmd = "MEASure:VOLTage?"
                    m_volt = m_visa.QueryCommand(send_cmd)
                    m_volt = m_volt.replace('\n', '').replace('\r', '')
                    send_cmd = "MEASure:CURRent?"
                    m_curr = m_visa.QueryCommand(send_cmd)
                    m_curr = m_curr.replace('\n', '').replace('\r', '')
                    if i ==0:
                        execution_time = 0.0
                        start_time = datetime.datetime.now()
                    else:
                        execution_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

                    index = i
                    print("%08d,%08d,%f,%f,%f" % (index, execution_time, float(m_volt), float(m_curr),(float(m_volt)*float(m_curr))))
                    writer.writerow([index, execution_time, float(m_volt), float(m_curr),(float(m_volt)*float(m_curr))])
                    i = i + 1
                    sleep(Delay)

            if IsOnOff == 'YES':
                send_cmd = "OUTPut %s;*OPC?" % 'OFF'
                m_return = m_visa.QueryCommand(send_cmd)

        send_cmd = "SYSTem:ERRor?"
        m_return = m_visa.QueryCommand(send_cmd)

        if m_return.find("No error") != -1:
            print("SUCCESS")
        else:
            print("FALSE")

    if bIsHelp:
        print("###################################################")
        print("############# Version: %s       #############" % Version)
        print("############# Built Date: %s  #############" % Built_Date)
        print("###################################################")
        print("PARAM 1: ON/OFF, Output ON/OFF")
        print("PARAM 2: Address, GPIB Address of Power supply")
        print("PARAM 3: Output, Output port of Power supply")
        print("PARAM 4: Voltage, Voltage Setting")
        print("PARAM 5: Current, Current limit setting")
        print("ex: PPS_GPIB.exe ON 5 1 3.8 2.0")
        print("ex: PPS_GPIB.exe OFF 5 1")
        print("\n###################################################\n")
        print("PARAM 1: ON/OFF/MEAS, Output ON/OFF/MEAS")
        print("PARAM 2: Address, GPIB Address of Power supply")
        print("PARAM 3: Output, Output port of Power supply")
        print("PARAM 4: Auto ON\OFF output")
        print("PARAM 5: Meas. Timeout ms")
        print("PARAM 6: Meas. Delay ms")
        print("ex: PPS_GPIB.exe MEAS 5 1 YES(ON\OFF) 10000 0")
        print("ex: PPS_GPIB.exe MEAS 5 1 YES(ON\OFF) 10000 0")
        if not bIsParmDone:
            print("ARGS_FALSE")