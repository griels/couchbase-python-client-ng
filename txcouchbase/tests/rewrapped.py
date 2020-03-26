import asyncio

from txcouchbase.bucket import TxCluster


class RewrappedCluster(TxCluster):
    def __init__(self, *args, **kwargs):
        async def wrapper():
            return super(RewrappedCluster, self).__init__(*args,**kwargs)
        self.evloop = asyncio.get_event_loop()
        self.evloop.run_until_complete(wrapper())
    async def wrapper(self, meth, *args, **kwargs):
        result=meth(super(RewrappedCluster,self), *args, **kwargs)
        return await result
    def _wrap(self,  # type: TxDeferredClient
              meth, *args, **kwargs):
        """
        Wraps a Twisted Cluster back into a synchronous cluster,
        for testing purposes
        """
        #if not self.connected:
        #    return self._connectSchedule(self._wrap, meth, *args, **kwargs)


        result=self.evloop.run_until_complete(self.wrapper(meth, *args, **kwargs))
        return result

    ### Generate the methods
    def _meth_factory(meth, name):
        def ret(self, *args, **kwargs):
            return self._wrap(meth, *args, **kwargs)
        return ret

    locals().update(TxCluster._gen_memd_wrappers(_meth_factory))
    for x in TxCluster._MEMCACHED_OPERATIONS:
        if locals().get(x+'_multi', None):
            locals().update({x+"Multi": locals()[x+"_multi"]})