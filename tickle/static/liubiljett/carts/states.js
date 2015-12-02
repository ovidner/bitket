'use strict'

angular.module('liubiljett.carts.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.cart',
        url: 'cart/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/carts/templates/cart.main.html'),
            controller: 'CartController as ctrl'
          }
        },
        resolve: {
          cart: ['SessionService',
            function (SessionService) {
              return SessionService.getCurrentCart()
            }]
        }
      }
    ].forEach($stateProvider.state)
  }
])
