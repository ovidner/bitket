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
        name: 'liubiljett.auth',
        abstract: true,
        resolve: {
          redirectUrl: ['$state',
            function ($state) {
              return $state.href($state.current.name, $state.current.params)
            }
          ]
        }
      },
      {
        name: 'liubiljett.auth.login',
        abstract: true
      },
      {
        name: 'liubiljett.auth.login.liu',
        url: '_saml/login/',
        onEnter: ['redirectUrl',
          function (redirectUrl) {
            window.location = '/_saml/login/?next=' + redirectUrl
          }
        ]
      },
      {
        name: 'liubiljett.auth.login.facebook',
        url: 'auth/facebook/login/',
        onEnter: ['redirectUrl',
          function (redirectUrl) {
            window.location = '/auth/facebook/login/?next=' + redirectUrl
          }
        ]
      },
      {
        name: 'liubiljett.auth.logout',
        url: 'logout/',
        onEnter: ['redirectUrl',
          function (redirectUrl) {
            window.location = '/logout/?next=' + redirectUrl
          }
        ]
      }
    ].forEach($stateProvider.state)
  }
])
