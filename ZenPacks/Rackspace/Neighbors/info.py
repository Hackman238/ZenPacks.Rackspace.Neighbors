# This file is the conventional place for "Info" adapters. Info adapters are
# a crucial part of the Zenoss API and therefore the web interface for any
# custom classes delivered by your ZenPack. Examples of custom classes that
# will almost certainly need info adapters include datasources, custom device
# classes and custom device component classes.

# Mappings of interfaces (interfaces.py) to concrete classes and the factory
# (these info adapter classes) used to create info objects for them are managed
# in the configure.zcml file.

from zope.interface import implements
from Products.Zuul.decorators import info
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from ZenPacks.Rackspace.Neighbors import interfaces

from Products.Zuul.interfaces import IInfo

import logging
log = logging.getLogger('NeighborsLink')


class NeighborsLinkInfo(ComponentInfo):
    implements(interfaces.INeighborsLink)

    NeighborsType = ProxyProperty("NeighborsType")
    locPortDesc = ProxyProperty("locPortDesc")
    remSysName = ProxyProperty("remSysName")
    remPortDesc = ProxyProperty("remPortDesc")
    remMgmtAddr = ProxyProperty("remMgmtAddr")

    @property
    @info
    def localInterface(self):
        interface = self._object.localInterface()
        try:
            log.warn("localInterface Info for %s the name is %s" % \
                (interface, interface.name))
        except:
            log.warn("localInterface Info can't log")
        return interface

    @property
    @info
    def remoteInterface(self):
        return self._object.remoteInterface()

    @property
    @info
    def remoteDevice(self):
        return self._object.remoteDevice()

    @property
    @info
    def remoteIp(self):
        return self._object.remoteIp()

    monitor = False  # not polled, only during model, no graphs
