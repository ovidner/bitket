'use strict'

angular.module('liubiljett.events.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.organizer',
        url: 'events/{organizerId}/',
        abstract: true
      },
      {
        name: 'liubiljett.organizer.event',
        url: '{eventId}/',
        views: {
          'main@': {
            templateUrl: StaticFile(
              'liubiljett/events/templates/organizer.event.main.html'),
            controller: 'EventController as ctrl'
          }
        },
        resolve: {
          event: ['$stateParams', 'Restangular',
            function ($stateParams, Restangular) {
              return Restangular.one('organizers', $stateParams.organizerId).one('main-events', $stateParams.eventId).get()
            }],
          products: ['event',
            function (event) {
              return event.all('products').getList()
            }]
        }
      }
    ].forEach($stateProvider.state)
  }])
