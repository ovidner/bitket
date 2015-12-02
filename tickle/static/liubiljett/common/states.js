'use strict'

angular.module('liubiljett.common.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett',
        abstract: true
      }
    ].forEach($stateProvider.state)
  }
])
