__doc__ = """A Layer2 Link discovered by CDP or Other Methods (LLDP) for now a OS Component"""

__version__ = "0.1"

# from Globals import DTMLFile
# from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

# from Products.ZenModel.DeviceComponent import DeviceComponent
# from Products.ZenModel.ManagedEntity import ManagedEntity

from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenUtils.Utils import prepId
from Products.ZenModel.ZenossSecurity import *
from AccessControl import ClassSecurityInfo 

import logging
log = logging.getLogger('NeighborsLink')


class NeighborsLink(OSComponent):
    """Neighbors Link information"""

    portal_type = meta_type = 'NeighborsLink'

    _properties = OSComponent._properties + (
        {'id': 'NeighborsType', 'type': 'string', 'mode': ''},
        {'id': 'locPortDesc', 'type': 'string', 'mode': ''},
        {'id': 'locIndex',    'type': 'string', 'mode': ''},
        {'id': 'remPortDesc', 'type': 'string', 'mode': ''},
        {'id': 'remSysName',  'type': 'string', 'mode': ''},
        {'id': 'remMgmtAddr', 'type': 'string', 'mode': ''},
        )

    _relations = OSComponent._relations + ((
        "os",
        ToOne(ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "neighborslinks")
        ),)

    NeighborsType = "unknown"
    locPortDesc = "unknown"
    locIndex = ""
    remPortDesc = "unknown"
    remSysName = "unknown"
    remMgmtAddr = "unknown"
    remlink = "unknown"


    def remoteIp(self):
        """get IpInterface Object for remote address"""
        if not self.remMgmtAddr:
            return None
        log.warn("searching for ip %s" % self.remMgmtAddr)
        ip = self.dmd.Networks.findIp(self.remMgmtAddr)
        log.warn("found %s" % ip)
        return ip

    def interfaceByDesc(self, device, desc):
        try:
            interface = device.os.interfaces._getOb(prepId(desc))
        except:
            # catch all, bad, but lazy
            log.warn("can't find interface %s on device %s" % (desc, device))
            return desc
        return interface

    def localInterface(self):
        #log.warn("localInterface called")
        return self.interfaceByDesc(self.device(), self.locPortDesc)

    def remoteDevice(self):
        """try to get the remote device, using the management IP"""
        ip = self.remoteIp()
        if ip:
            if ip.device() is None:
                return self.remSysName
            else:
                return ip.device()
        else:
            return self.remSysName

    def remoteInterface(self):
        ip = self.remoteIp()
        if not ip:
            return self.remPortDesc
        device = ip.device()
        if not device:
            return self.remPortDesc
        return self.interfaceByDesc(device, self.remPortDesc)

InitializeClass(NeighborsLink)
