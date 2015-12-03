'use strict'

angular.module('liubiljett.people.directives', [])

.directive('lbPersonMenu', ['SessionService',
  function (SessionService) {
    return {
      scope: {},
      templateUrl: StaticFile('liubiljett/people/templates/directives/lb-person-menu.html'),
      link: function (scope, element, attrs, controllers) {
        SessionService.getCurrentPerson().then(function (person) {
          scope.person = person
        })
      }
    }
  }
])
