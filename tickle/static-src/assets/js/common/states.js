'use strict'

angular.module('liubiljett.common.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett',
        url: '/',
        abstract: true
      }
    ].forEach($stateProvider.state)
  }
])
