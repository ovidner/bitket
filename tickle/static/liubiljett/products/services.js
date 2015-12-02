'use strict'

angular.module('liubiljett.products.services', [])

.factory('Holding', ['Restangular',
  function (Restangular) {
    return Restangular.service('holdings')
  }
])
