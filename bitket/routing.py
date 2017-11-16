from channels.routing import include, route

channel_routing = [
    include('cq.routing.channel_routing'),
]
