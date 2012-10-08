(function() {

var ZC = Ext.ns('Zenoss.component');
function render_link(ob) {
    if (ob && ob.uid) {
        /* we also need a name! */
        if (ob.name) {
            name = ob.name;
        } else {
            /* extract from object */
            var parts = ob.uid.split('/');
            name = parts[parts.length-1];
        }
        return Zenoss.render.link(ob.uid,null,name);
    } else {
        return ob;
    }
}
 


ZC.NeighborsLinkPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NeighborsLink',
            autoExpandColumn: 'remoteInterface',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'localInterface'},
                {name: 'remoteInterface'},
                {name: 'remoteDevice'},
                {name: 'remoteIp'},
                {name: 'NeighborsType'},
            ],
            columns: [{
                id: 'NeighborsType',
                dataIndex: 'NeighborsType',
                header: _t('Neighbor Protocol'),
                width: 150,
                renderer: render_link
            },{
                id: 'localInterface',
                dataIndex: 'localInterface',
                header: _t('Local Interface'),
                width: 150,
                renderer: render_link
            },{
                id: 'remoteDevice',
                dataIndex: 'remoteDevice',
                header: _t('Remote Device'),
                width: 150,
                renderer: render_link
            },{
               	id: 'remoteIp',
                dataIndex: 'remoteIp',
                header: _t('Remote IP'),
                width: 150,
                renderer: render_link
            },{
                id: 'remoteInterface',
                dataIndex: 'remoteInterface',
                header: _t('Remote Interface'),
                renderer: render_link
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                width: 72,
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.NeighborsLinkPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('NeighborsLinkPanel', ZC.NeighborsLinkPanel);
ZC.registerName('NeighborsLink', _t('NeighborsLink Interface'), _t('Neighbors'));

}());
