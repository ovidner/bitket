'use strict'

angular.module('liubiljett.home.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.home',
        url: '',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/home/templates/home.main.html')
          }
        }
      }
    ].forEach($stateProvider.state);
  }
])
