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
      },
      {
        name: 'liubiljett.holding',
        abstract: true
      },
      {
        name: 'liubiljett.holding.detail',
        url: 'holdings/{holdingId}/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/holding.detail.main.html'),
            controller: 'HoldingDetailController as ctrl'
          }
        },
        resolve: {
          holding: ['$stateParams', 'Restangular',
            function ($stateParams, Restangular) {
              return Restangular.one('holdings', $stateParams.holdingId).get()
            }
          ]
        }
      },
      {
        name: 'liubiljett.holding.utilize',
        url: 'utilize/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/holding.utilize.main.html'),
            controller: 'UtilizeController as ctrl'
          }
        }
      }
    ].forEach($stateProvider.state)
  }
])
