'use strict'

angular.module('liubiljett.products.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.cart',
        url: 'cart/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/cart.main.html'),
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
