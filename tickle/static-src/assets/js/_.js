'use strict'

angular.module('liubiljett', [
    // Third party modules
  'ngRaven',
  'ui.router',
  'ngMaterial',
  'ct.ui.router.extras',
  'hc.marked',
  'restangular',
  'credit-cards',
  'angular-stripe',

  // liubiljett modules
  'liubiljett.common',
  'liubiljett.events',
  'liubiljett.home',
  'liubiljett.people',
  'liubiljett.products'
])

.config(['$httpProvider', '$locationProvider', '$urlMatcherFactoryProvider',
  '$urlRouterProvider', '$mdThemingProvider', '$stickyStateProvider',
  'RestangularProvider',
  function ($httpProvider, $locationProvider, $urlMatcherFactoryProvider,
            $urlRouterProvider, $mdThemingProvider, $stickyStateProvider,
            RestangularProvider) {
    $stickyStateProvider.enableDebug(true)
    // Enables "real" URLs like /dashboard/ instead of /#/dashboard/
    $locationProvider.html5Mode(true)
    // Disables stripping of trailing slash in routers. Needed for headache-
    // free cooperation with Django.
    $urlMatcherFactoryProvider.strictMode(false)

    // Sets CSRF token cookie and header name to work with Django.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken'
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'

    RestangularProvider.setBaseUrl('/api')
    RestangularProvider.setRequestSuffix('/')
    RestangularProvider.setRestangularFields({
      selfLink: 'url'
    })

    $mdThemingProvider.theme('default')
      .primaryPalette('blue')
      .accentPalette('pink')
      .warnPalette('amber')

    $mdThemingProvider.theme('inverted')
      .primaryPalette('pink')
      .accentPalette('blue')
  }])
