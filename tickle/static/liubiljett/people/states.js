'use strict'

angular.module('liubiljett.people.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.person',
        abstract: true
      },
      {
        name: 'liubiljett.login',
        abstract: true,
        resolve: {
          redirectUrl: ['$state',
            function ($state) {
              return $state.current.href
            }
          ]
        }
      },
      {
        name: 'liubiljett.login.liu',
        url: '_saml/login/',
        onEnter: ['redirectUrl',
          function (redirectUrl) {
            window.location = '/_saml/login/' + '?next=' + redirectUrl
          }
        ]
      }
    ].forEach($stateProvider.state)
  }
])
