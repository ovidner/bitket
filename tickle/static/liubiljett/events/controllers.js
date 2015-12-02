'use strict'

angular.module('liubiljett.events.controllers', [])

.controller('EventController', ['event', 'products',
  function (event, products) {
    var ctrl = this
    ctrl.event = event
    ctrl.event.products = products
  }
])
