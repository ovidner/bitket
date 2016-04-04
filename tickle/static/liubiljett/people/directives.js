'use strict'

angular.module('liubiljett.people.directives', [])

.directive('lbPersonMenu', ['$mdDialog', 'SessionService',
  function ($mdDialog, SessionService) {
    return {
      scope: {},
      templateUrl: StaticFile('liubiljett/people/templates/directives/lb-person-menu.html'),
      link: function (scope, element, attrs, controllers) {
        SessionService.getCurrentPerson().then(function (person) {
          scope.person = person
        })

        var loginDialog = {
          autoWrap: false,
          clickOutsideToClose: true,
          controller: function () {
            this.hide = function () {
              $mdDialog.hide()
            }
          },
          controllerAs: 'dialog',
          bindToController: true,
          templateUrl: StaticFile('liubiljett/people/templates/dialogs/loginDialog.html')
        }

        scope.openLoginDialog = function () {
          $mdDialog.show(loginDialog)
        }
      }
    }
  }
])
