'use strict';

angular.module('liubiljett.common.controllers', [])

.controller('MainToolbarCtrl', ['$mdSidenav',
  function ($mdSidenav) {
    var ctrl = this;

    ctrl.toggleSidenav = function (componentId) {
      $mdSidenav(componentId).toggle();
    };
  }
]);
