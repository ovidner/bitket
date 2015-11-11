'use strict';

angular.module('liubiljett', [
    // Third party modules
  'ui.router',
  'ngMaterial',
  'ct.ui.router.extras',
  'hc.marked',

  // liubiljett modules
  'liubiljett.common',
  'liubiljett.events',
  'liubiljett.home',
  'liubiljett.products',
])

.config(['$httpProvider', '$locationProvider', '$urlMatcherFactoryProvider',
  '$urlRouterProvider', '$mdThemingProvider', '$stickyStateProvider',
  function ($httpProvider, $locationProvider, $urlMatcherFactoryProvider,
            $urlRouterProvider, $mdThemingProvider, $stickyStateProvider) {
    $stickyStateProvider.enableDebug(true);
    // Enables "real" URLs like /dashboard/ instead of /#/dashboard/
    $locationProvider.html5Mode(true);
    // Disables stripping of trailing slash in routers. Needed for headache-
    // free cooperation with Django.
    $urlMatcherFactoryProvider.strictMode(false);

    // Sets CSRF token cookie and header name to work with Django.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $mdThemingProvider.theme('default')
      .primaryPalette('blue')
      .accentPalette('pink')
      .warnPalette('yellow');

    $mdThemingProvider.theme('inverted')
      .primaryPalette('pink')
      .accentPalette('blue');
  }]);
