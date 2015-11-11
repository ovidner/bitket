'use strict';

angular.module('liubiljett.common.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    var states = [
      {
        name: 'liubiljett',
        abstract: true
      }
    ];

    angular.forEach(states, function (state) {
      $stateProvider.state(state);
    });
  }
]);
