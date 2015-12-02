'use strict'

angular.module('liubiljett.carts.controllers', [])

.controller('CartController', ['cart',
  function (cart) {
    var ctrl = this
    ctrl.cart = cart
  }
])
