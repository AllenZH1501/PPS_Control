# This is a sample Python script.
import pyvisa
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
Version = '1.00.001'
Built_Date = "2022/04/08"
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bIsParmDone = False
    bIsHelp = False
    if len(sys.argv) == 1:
        bIsHelp = True
        bIsParmDone = False
    elif len(sys.argv) == 2:
        if sys.argv[1].find("?") != -1 or sys.argv[1].find("-help") != -1  or sys.argv[1].find("-h") != -1:
            bIsHelp = True
            bIsParmDone = False
    else:
        if len(sys.argv) > 2:
            sonoff = sys.argv[1]
            saddress = sys.argv[2]
            soutput = sys.argv[3]
            bIsParmDone = True
            if sonoff == 'ON':
                if len(sys.argv) > 5:
                    svolt = sys.argv[4]
                    scurr = sys.argv[5]
                    bIsParmDone = True
                else:
                    bIsParmDone = False
                    bIsHelp = True
        else:
            bIsParmDone = False
            bIsHelp = True


    if bIsParmDone:
        m_rm = pyvisa.ResourceManager()
        m_rm.list_resources()

        connectstr = "GPIB0::%s::INSTR" % saddress
        m_inst = m_rm.open_resource(connectstr)

        send_cmd = ""

        send_cmd = "*IDN?"
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "*CLS;*OPC?"
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "INST:SEL OUT%s;*OPC?" % soutput
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "INST:SEL?"
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        if sonoff == 'ON':
            send_cmd = "VOLT %s;*OPC?" % svolt
            print("[SEND]: %s" % send_cmd)
            m_return = m_inst.query(send_cmd)
            print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

            send_cmd = "CURR %s;*OPC?" % scurr
            print("[SEND]: %s" % send_cmd)
            m_return = m_inst.query(send_cmd)
            print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

            send_cmd = "VOLT?"
            print("[SEND]: %s" % send_cmd)
            m_return = m_inst.query(send_cmd)
            print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

            send_cmd = "CURR?"
            print("[SEND]: %s" % send_cmd)
            m_return = m_inst.query(send_cmd)
            print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "OUTPut %s;*OPC?" % sonoff
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "OUTPut?"
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

        send_cmd = "SYSTem:ERRor?"
        print("[SEND]: %s" % send_cmd)
        m_return = m_inst.query(send_cmd)
        print("[RETU]: %s" % m_return.replace('\n', '').replace('\r', ''))

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
        if not bIsParmDone:
            print("PARMS_FALSE")