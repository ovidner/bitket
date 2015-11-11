'use strict';

angular.module('liubiljett.people.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    var states = [
    {
      name: ''
    }];

    angular.forEach(states, function (state) {
      $stateProvider.state(state);
    });
  }
]);
