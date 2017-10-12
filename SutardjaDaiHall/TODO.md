# SDH TODO

## TODO

- air handler units
- chillers
- "controls" relationships
- HEAT.COOL
- close the HVAC loop on the return fans:
    - do we have return fans?
- add constant volume vavs
- exhaust fans (EF1, EF2,...)

## Notes

### Info from Paul

- AHU to VAV mapping:
    - right now this is made up; get from Paul?
    - ANSWER: these are in parallel; AH2A/B feed all VAVs.
    - AH1A/1B go to the RAHUs. This is RHC
    - CCV is constant volume terminal unit
    - 2 chillers feed whole building
    - most zones have reheat; if there's a damper its a vav not a cv
    - CLG/HTG Loopout are PID outputs
    - for control, you write to HEAT.COOL first, and then do the setpoint
- RHC:
    - right now these are all associated with AH1;
    - is this correct? Are they external to the AHU? Internal?
    - what does HEAT.COOL mean
- RAH:
    - are these a type of VAV? Are they another piece of equipment?
    - how do these map to zones/rooms?

### Other info

AH1A,AH1B: feed the nano fab lab
AH2A,AH2B: feed the offices

`/Siemens/SDH.PXCM-11/SDH/S3-07/AI_3`: 
Discharge air temperature sensor on the VAV box 

`/Siemens/SDH.PXCM-11/SDH/S3-07/CTL_STPT`:
The current air temperature control setpoint

`/Siemens/SDH.PXCM-11/SDH/S3-07/HEAT.COOL`: 
What the last active conditioning mode of the VAV box was. e.g. heating (value=1)  or cooling (value=0). This determines what the value of `CTL_STPT` represents - either the heating or cooling setpoint. 
think of this as "mode"

---

## CHiller notes

2 cooling towers; 1 for each chiller

CHP3,4,5 are all pumps; they pump water to the valve

chillers bypass valve; connects both chillers?
chilled water flow chx; flow for both?

take another pass through and find those

schedule meeting w/ domenico

pumps:
cwp1,2,3,4
chp1,2,3,4

chp2, cwp3 are for absorption chiller (ch1)

chp1, cwp1 are for centrifugal chiller (ch2)

In October 2012, variable frequency drives were added to one of the two chilled water and condenser water pumps for each chiller: CHP-2 and CWP-3 for the absorption chiller (CH1) and CHP-1 and CWP-1 for the centrifugal chiller (CH2)[1]. These VFDs provide turndown control as well as submetering the power consumption of the device.


[1] Note that each chiller has two chilled water pumps and two condenser water pumps that were designed to run in a lead-lag fashion (alternating one on for a week then the other). Because the resources to add VFDs were limited, only one of each pump were retrofitted with a VFD. This pump now runs nearly every day, but one day of the month the other pump is used.


## Hot Water System

look for "\.hw" 

feeds each VAV directly?

## VAVs

~~TODO: room valve position is HEATING valve!!~~

~~`ai_3`: discharge air temperature~~

## AHU Notes

air handler unit:
- return:
    - sensors:
        - return air temp
        - return air humidity
        - return duct static pressure sensor
        - return air flow sensor
        - return air humidity sensor
    - fan:
        - return fan speed
        - return fan power
    - damper:
        - return air damper

- exhaust:
    - damper:
        - exhaust air damper
        - outside air damper
            - minimum outside air damper position
        - isolation damper

- mixed:
    - sensors:
        -mixed air temperature sensor

- supply:
    - sensors:
        - supply air temp setpoint
        - supply air temp
        - supply air flow
        - supply duct static pressure sensor
    - fan:
        - supply fan speed
        - supply fan power


layout:
- make dampers:
    - return, exhaust, outside, isolation, supply
    - ahu "has part" to all of these
- ahu 'has point' sensors too
- things feeding air handler unit
    - return fan FEEDS return damper FEEDS ahu
    - outside air damper FEEDS ahu
- ahu feeds:
    - ahu FEEDS supply fan

points:
    damper:
        - position command ; position state
        - temperature sensor?
    fan:
        - speed
        - power
