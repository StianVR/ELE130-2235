# coding=utf-8

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import sys
import json
try:
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ----> Husk å oppdatere denne !!!!!!!!!!!!!!
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    from P00_TestOppkopling import MathCalculations
except Exception as e:
    pass
    # print(e)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     A) online and offline: SET ONLINE FLAG, IP-ADRESSE OG FILENAME
#
online = False

# Hvis online = True, pass på at IP-adresse er satt riktig.
EV3_IP = "169.254.183.102"

# Hvis online = False, husk å overføre filen med målinger og 
# eventuelt filen med beregnede variable fra EV3 til datamaskinen.
# Bruk 'Upload'-funksjonen

# --> Filnavn for lagrede MÅLINGER som skal lastes inn offline
filenameMeas = "Meas_P00_matplotlib_1.txt"

# --> Filnavn for lagring av BEREGNEDE VARIABLE som gjøres offline
#     Typisk navn:  "CalcOffline_P0X_BeskrivendeTekst_Y.txt"
#     Dersom du ikke vil lagre BEREGNEDE VARIABLE, la det stå 
#     filenameCalcOffline = ".txt"
filenameCalcOffline = ".txt"
#---------------------------------------------------------------------


if not online:    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       B) offline: MEASUREMENTS. INTITALIZE LISTS ACCORDING TO 6)
    # 
    # Denne seksjonen kjøres kun i offline og initialiserer TOMME
    # lister for MÅLINGENE som pakkes opp fra .txt-filen i seksjon
    #   -->  E) offline: UNPACK MEASUREMENTS FROM FILE ACCORDING TO 6)
    # nedenfor.
    # 
    # Velg variabelnavn for listene identiske med de som lagres 
    # i .txt-filen i seksjon
    #   --> 6) STORE MEASUREMENTS TO FILE
    # i hovedfilen. 

    Tid = []
    Lys = []
    VinkelPosMotorA = []
    HastighetMotorA = []
    joyForward = []
    joySide = []
    joy2 = []
    
    print("B) offline: MEASUREMENTS. LISTS INTITALIZED.")
    #---------------------------------------------------------------------

    
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #   C) offline: OWN VARIABLES. INITIALIZE LISTS
    #
    # Denne seksjonen kjøres kun i offline og initialiserer 
    # lister med EGNE VARIABLE i offline-modus. Tenk nøye 
    # gjennom hvilke lister som skal ha en initialverdi.
    # 
    # Dersom du i onlineversjonen av prosjektet benyttet seksjonen
    #      --> 4) optional: OWN VARIABLES. INITIALIZE LISTS
    # i hovedfilen, så bør variabelnavnene på like lister være
    # identiske i seksjon 4) og C). Dette fordi koden blir 
    # oversiktlig. Du kan selvfølgelig legge til nye lister med
    # EGNE VARIABLE her i denne seksjonen når du kjører prosjektet
    # offline.
    
    Pos_vs_Hastighet = []
    Forward_vs_Side = []
    summeringAvPowerA = [0]
    PowerA = []
    mellomRegninger = []
    
    print("C) offline: OWN VARIABLES. LISTS INITIALIZED.")
    #---------------------------------------------------------------------
    
else:
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     D) online: DATA TO PLOT. INITIALIZE LISTS ACCORDING TO 9)
    #     
    # Denne seksjonen kjøres kun i online og initialiserer TOMME
    # lister med DATA hvor du velger variabelnavn identisk med   
    # de som er brukt på MÅLINGER og EGNE VARIABLE i hovedfilen 
    # i seksjon
    #  --> 9) wired only: SEND DATA TO F) FOR PLOTTING
    # 
    # DATAene sendes fra hovedfilen til seksjon
    #  --> F) online: RECEIVE DATA TO PLOT ACCORDING TO 9) 
    # nedenfor.
    #
    # For å holde orden i koden bør du benytte samme 
    # struktur/rekkefølge i seksjonene 9), D) og F)

    # målinger
    Tid = []
    HastighetMotorA = []
    
    # egne variable
    PowerA = []
    summeringAvPowerA = []
    Forward_vs_Side = []
    Pos_vs_Hastighet = []
    
    print("D) online: LISTS FOR DATA TO PLOT INITIALIZED.")
    #---------------------------------------------------------------------


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     E) offline: UNPACK MEASUREMENTS FROM FILE ACCORDING TO 6)
#
# Denne seksjonen kjøres kun i offline, og her pakkes ut
# MÅLINGER som ble lagret i seksjon  
#  --  6) STORE MEASUREMENTS TO FILE
# i hovedfilen.
#
# For å holde orden i koden bør du benytte samme struktur/rekkefølge
# i seksjonene E) og 6).
# 
# Det er viktig å spesifisere riktig datatype og kolonne
# for hver utpakket liste.
def unpackMeasurement(rowOfMeasurement):
    Tid.append(float(rowOfMeasurement[0]))
    Lys.append(int(rowOfMeasurement[1]))
    VinkelPosMotorA.append(float(rowOfMeasurement[2]))
    HastighetMotorA.append(float(rowOfMeasurement[3]))
    joyForward.append(float(rowOfMeasurement[4]))
    joySide.append(float(rowOfMeasurement[5]))
    joy2.append(str(rowOfMeasurement[6]))

#-------------------------------------------------------------


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      F) online: RECEIVE DATA TO PLOT ACCORDING TO 9) 
#
# Denne seksjonen kjøres kun i online, og her pakkes ut 
# DATA som sendes over fra seksjon 9) i hovedfilen.
# 
# For å holde orden i koden bør du benytte samme struktur/rekkefølge
# som i seksjonen
#   --> 9) wired only: SEND DATA TO F) FOR PLOTTING

def unpackData(rowOfData):

    # målinger
    Tid.append(rowOfData["Tid"])
    HastighetMotorA.append(rowOfData["HastighetMotorA"])

    # egne variable
    PowerA.append(rowOfData["PowerA"])
    summeringAvPowerA.append(rowOfData["summeringAvPowerA"])
    Forward_vs_Side.append(rowOfData["Forward_vs_Side"])
    Pos_vs_Hastighet.append(rowOfData["Pos_vs_Hastighet"])
                
#-------------------------------------------------------------



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      G) online and offline: PLOT DATA
# 
# Først spesifiseres selve figuren. Dersom enten nrows = 1 
# eller ncols = 1, så gis ax 1 argument som ax[0], ax[1], osv.
# Dersom både nrows > 1 og ncols > 1,  så må ax gis 2 argumenter 
# som ax[0,0], ax[1,0], osv
fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True)

# Vær obs på at ALLE delfigurene må inneholde data. 
# Repeter om nødvendig noen delfigurer for å fylle ut.
def figureTitles():
    global ax
    ax[0,0].set_title('HastighetMotorA')
    ax[0,1].set_title('PowerA')
    ax[1,0].set_title('Summering av PowerA')
    ax[1,1].set_title('Forward vs side joystick')
    ax[2,0].set_title('Posisjon vs hastigmet motor A')

    # Gjentar siste data en gang til
    ax[2,1].set_title('Posisjon vs hastigmet motor A')

    ax[2,0].set_xlabel('Tid [sec]')
    ax[2,1].set_xlabel('Tid [sec]')


# Vær obs på at ALLE delfigurene må inneholde data. 
# Repeter om nødvendig noen delfigurer for å fylle ut.
def plotData():
    ax[0,0].plot(Tid[0:], HastighetMotorA[0:], 'b')
    ax[0,1].plot(Tid[0:], PowerA[0:], 'b')
    ax[1,0].plot(Tid[0:], summeringAvPowerA[0:], 'b')
    ax[1,1].plot(Tid[0:], Forward_vs_Side[0:], 'b')
    ax[2,0].plot(Tid[0:], Pos_vs_Hastighet[0:], 'b')

    # Gjentar siste data en gang til
    ax[2,1].plot(Tid[0:], Pos_vs_Hastighet[0:], 'b')
#---------------------------------------------------------------------


def stopPlot():
    try:
        livePlot.event_source.stop()
    except:
        pass


def offline(filenameMeas, filenameCalcOffline):
    # Hvis offline

    with open(filenameMeas) as f:
        # Leser inn målingene fra fil inn i MeasurementFromFile.
        # Fjerner de 4 første linjene som er reservert til header.
        MeasurementFromFile = f.readlines()[4:]
                        
        # Går inn i "løkke"
        for EachRow in MeasurementFromFile:
            # Pakk ut målingene 
            rowOfMeasurement = EachRow.split(",")
            unpackMeasurement(rowOfMeasurement)
            
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #   H) offline: PERFORM CALCULATIONS 
            # 
            # Denne seksjonen kjøres kun i offline og den baserer seg 
            # på målingene som pakkes ut i seksjon
            #  --> E) offline: UNPACK MEASUREMENTS FROM FILE ACCORDING TO 6)
            # og listene over EGNE VARIABLE definert i seksjon
            #  --> C) offline: OWN VARIABLES. INITIALIZE LISTS
            #
            # Denne seksjonen kaller MathCalculations() i seksjon
            #       --> 12) MATH CALCULATIONS
            # i hovedfilen. Pass på at funksjonskallet og beskrivelsen 
            # er identisk i H) og 12) når det kjøres offline.
            #
            # Siden motor(er) ikke brukes offline, så sendes IKKE 
            # beregnet pådrag til motor(ene), selv om pådraget 
            # kan beregnes og plottes.

            MathCalculations(Tid, Lys, VinkelPosMotorA, HastighetMotorA, 
                joyForward, joySide, joy2, PowerA, summeringAvPowerA,
                Forward_vs_Side, Pos_vs_Hastighet, mellomRegninger)
            #---------------------------------------------------------

        # Eksperiment i offline er nå ferdig

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #          I) offline: STORE CALCULATIONS FROM H) TO FILE
        #
        # Denne seksjonen kjøres kun i offline, og den kjøres ETTER
        # at offline-eksperimentet i er ferdig. De mulige variable
        # som kan lagres er de som beregnes i seksjonen
        #    --> H) offline: PERFORM CALCULATIONS 
        # ovenfor.
        #
        # Dersom du ikke ønsker å lagre EGEN VARIABLE i denne 
        # seksjonen, la filnavnet for lagring av beregnede variable
        # være tomt
        
        # Vi legger først inn 3 linjer som header i filen med beregnede 
        # variable. Du kan legge inn flere linjer om du vil.
        if len(filenameCalcOffline)>4:
            with open(filenameCalcOffline, "w") as f:
                CalculatedToFileHeader = "Tallformatet viser til kolonnenummer:\n"
                CalculatedToFileHeader += "0=Pos_vs_Hastighet, 1=Forward_vs_Side, \n"
                CalculatedToFileHeader += "2=summeringAvPowerA, 3=powerA, 4=mellomRegninger \n"
                f.write(CalculatedToFileHeader)

                # Lengde av de MÅLTE listene
                # Husk at siste element i strengen må være '\n'            
                for i in range(0,len(Tid)):
                    CalculatedToFile = ""
                    CalculatedToFile += str(Pos_vs_Hastighet[i]) + ","
                    CalculatedToFile += str(Forward_vs_Side[i]) + ","
                    CalculatedToFile += str(summeringAvPowerA[i]) + ","
                    CalculatedToFile += str(PowerA[i]) + ","
                    CalculatedToFile += str(mellomRegninger[i]) + "\n"
                    f.write(CalculatedToFile)
        #---------------------------------------------------------

    # Plot data (målinger og beregnede verdier) fra listene.
    figureTitles()
    plotData()
    stopPlot()
    # Set plot layout and show plot.
    fig.set_tight_layout(True)  # mac
    plt.show()



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#               IKKE ENDRE NOE UNDER HER
#---------------------------------------------------------------------


# Tmp data
tmp = ""

def live(i):
    global tmp
    # Recieve data from EV3.
    try:
        DataToOnlinePlot = sock.recv(1024)
    except Exception as e:
        print(e)
        print("Lost connection to EV3")
        stopPlot()
        return

    try:
        DataToOnlinePlot = DataToOnlinePlot.split(b"?")
        # Reconstruct split data
        if tmp != "":
            DataToOnlinePlot[0] = tmp + DataToOnlinePlot[0]
            tmp = ""
            print("Reconstructed data: ", DataToOnlinePlot[0])

        for rowOfData in DataToOnlinePlot:
            if rowOfData == b'':
                continue
            # If the data recieved is the end signal, freeze plot.
            elif rowOfData == b"end":
                print("Recieved end signal")
                stopPlot()
                return
            try:
                rowOfData = json.loads(rowOfData)
            except:
                # Save incomplete data
                tmp = rowOfData
                continue
            # Unpack the recieved row of data
            unpackData(rowOfData)
    except Exception as e:
        print(e)
        print("Data error")
        stopPlot()
        return

    # Plot the data in the lists.
    plotData()

if online:
    # If online, setup socket object and connect to EV3.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        addr = (EV3_IP, 8070)
        print("Attempting to connect to {}".format(addr))
        sock.connect(addr)
        DataToOnlinePlot = sock.recv(1024)
        if DataToOnlinePlot == b"ack":
            print("Connection established")
        else:
            print("no ack")
            sys.exit()
    except socket.timeout:
        print("failed")
        sys.exit()

    # Start live plotting.
    livePlot = FuncAnimation(fig, live, init_func=figureTitles(), interval=10)

    # Set plot layout and show plot.
    fig.set_tight_layout(True)
    plt.show()
else:
    # If offline, plot from file defined by filename.
    offline(filenameMeas,filenameCalcOffline)
