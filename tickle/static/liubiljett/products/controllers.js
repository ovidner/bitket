'use strict'

angular.module('liubiljett.products.controllers', [])

.controller('ProductController', ['Money', 'SessionService', 'Holding',
  function (Money, SessionService, Holding) {
    var ctrl = this
    ctrl.product.updatePrice()
  }
])
