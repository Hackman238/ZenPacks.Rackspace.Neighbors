__doc__ = """Model Layer 2 Links using CDP"""

__version__ = "0.1"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from struct import *


class CDPNeighborsMap(SnmpPlugin):
    """Map Layer 2 links using CDP"""

    maptype = "CDPNeighborsMap"
    modname = "ZenPacks.Rackspace.Neighbors.NeighborsLink"
    relname = "neighborslinks"
    compname = "os"

    snmpGetTableMaps = (
        GetTableMap('cdpLocPort',
                    '.1.3.6.1.4.1.9.9.23.1.1.1.1',
                    {
                        '.6': 'desc',
                    }
                    ),
        GetTableMap('ifLocPort',
                    '.1.3.6.1.2.1.2.2.1',
                    {
                        '.2': 'desc',
                    }
                    ),
        GetTableMap('cdpRemPort',
                    '.1.3.6.1.4.1.9.9.23.1.2.1.1',
                    {
                        '.7': 'desc',
                        '.6': 'sys',
                    }
                    ),
        GetTableMap('cdpRemMan',
                    '.1.3.6.1.4.1.9.9.23.1.2.1.1',
                    {
                        '.4': 'ifid',
                    }
                    ),
        )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        iflocPort = tabledata.get("ifLocPort")
        locPort = tabledata.get("cdpLocPort")
        remPort = tabledata.get("cdpRemPort")
        remMan = tabledata.get("cdpRemMan")
        rm = self.relMap()
        if not locPort:
            locPort = iflocPort
        if not remPort:
            log.info("no CDP information available")
            return rm
        if not locPort:
            log.info("CDP no local Ports found")
            return rm
        # prepare remIp
        remIps = {}
        for id, remote in remMan.items():
            idx = id.split(".")[0]
            try:
                ip = str(unpack('!4B',remote['ifid']))
                ip = ip.replace(",", ".")
                ip = ip.replace("(", "")
                ip = ip.replace(")", "")
                ip = ip.replace(" ", "")
                remIps[idx] = ip
            except:
                ip = ""
        for id, port in remPort.items():
            # extract the local index
            idx = id.split(".")[0]
            locDesc = locPort[idx].get("desc", "unknown")
            remSys = port.get("sys", "unknown")
            remDesc = port.get("desc", "unknown")
            remIp = remIps.get(idx, "")
            NeighborsType = "CDP"
            om = self.processLink(log, idx, locDesc, remSys, remDesc, remIp, NeighborsType)
            rm.append(om)
        return rm

    def processLink(self, log, locIdx, locDesc, remSys, remDesc, remIp, NeighborsType):
        log.info('found a link %s -> %s:%s' % (locDesc, remSys, remDesc))
        om = self.objectMap()
        om.id = self.prepId(locIdx)
        om.title = self.prepId(locDesc)
        om.locPortDesc = locDesc
        om.locIndex = locIdx
        om.remPortDesc = remDesc
        om.remSysName = remSys
        om.remMgmtAddr = remIp
        om.NeighborsType = NeighborsType
        return om
