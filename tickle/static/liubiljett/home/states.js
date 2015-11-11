'use strict';

angular.module('liubiljett.home.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    var states = [
      {
        name: 'liubiljett.home',
        url: '/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/home/templates/home.main.html')
          }
        }
      }
    ];

    angular.forEach(states, function (state) {
      $stateProvider.state(state);
    });
  }
]);
