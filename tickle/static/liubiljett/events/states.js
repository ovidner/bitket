'use strict';

angular.module('liubiljett.events.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    var states = [
      {
        name: 'liubiljett.organizer',
        url: '{organizerId}/',
        abstract: true
      },
      {
        name: 'liubiljett.organizer.event',
        url: '{eventId}/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/events/templates/organizer.event.main.html')
          }
        }
      }];

    angular.forEach(states, function (state) {
      $stateProvider.state(state);
    });
  }]);
