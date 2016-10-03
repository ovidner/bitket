'use strict'

angular.module('liubiljett.common.services', [])

.factory('Money', function () {
  var MoneyService = Big()
  MoneyService.DP = 2
  MoneyService.RM = 1
  return MoneyService
})
