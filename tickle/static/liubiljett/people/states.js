'use strict'

angular.module('liubiljett.people.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    var states = [
      {
        name: 'liubiljett.person',
        abstract: true
      }
    ]

    states.forEach($stateProvider.state)
  }
])
