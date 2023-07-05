#           MH-Z19 Plugin
#
#           Author:     tjonczyk, 2023
#

"""
<plugin key="MH-Z19" name="MH-Z19" author="tjonczyk" version="0.0.1">
    <description>
        MH-Z19 Sensor Plugin.<br/>
        Install mh_z19 python plugin before using this plugin.mh_z19.<br/>
        https://pypi.org/project/mh-z19/ (pip install mh_z19)<br/>
        https://bobbyhadz.com/blog/python-attributeerror-module-serial-has-no-attribute-serial<br/><br/>
        # 👇️ uninstall serial and pyserial<br/>
        pip uninstall serial<br/>
        pip uninstall pyserial<br/><br/>

        pip3 uninstall serial<br/>
        pip3 uninstall pyserial<br/><br/>

        # 👇️ install pyserial<br/>
        pip install pyserial<br/>
        pip3 install pyserial<br/><br/>
    </description>
</plugin>
"""

import mh_z19
import json
import Domoticz

class Mhz19Device:

    def getData(self):
        co2 = str(mh_z19.read())
        co2 = co2.replace("\'", "\"")
        Domoticz.Log("Mhz19Device - getData: " + co2)
        co2Json = json.loads(co2)
        co2Value = co2Json["co2"]
        return co2Value


class BasePlugin:
    deviceName = "Mhz19Device"

    def onStart(self):
        Domoticz.Log(self.deviceName + ": onStart")
        deviceFound = False
        for Device in Devices:
            if self.deviceName in Devices[Device].Name:
                deviceFound = True

        if deviceFound == False:
            Domoticz.Device(Name=self.deviceName,
                            Unit=len(Devices) + 1,
                            Type=243,
                            Subtype=31,
                            Options={"Custom": "1;<axisUnits>"}).Create()

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        m = Mhz19Device()
        data = m.getData()

        for Device in Devices:
            Domoticz.Log("onHeartbeat data: " + str(Devices[Device].Options))
            if self.deviceName in Devices[Device].Name:
                Domoticz.Log("update device:" + self.deviceName + ", with value: " + str(data))
                Devices[Device].Update(sValue=data)

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

