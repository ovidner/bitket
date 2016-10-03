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

'use strict'

angular.module('liubiljett.common', [
  'liubiljett.common.controllers',
  'liubiljett.common.directives',
  'liubiljett.common.services',
  'liubiljett.common.states'
])

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

'use strict';

angular.module('liubiljett.common.directives', []);

'use strict'

angular.module('liubiljett.common.services', [])

.factory('Money', function () {
  var MoneyService = Big()
  MoneyService.DP = 2
  MoneyService.RM = 1
  return MoneyService
})

'use strict'

angular.module('liubiljett.common.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett',
        url: '/',
        abstract: true
      }
    ].forEach($stateProvider.state)
  }
])

'use strict';

angular.module('liubiljett.events', [
  'liubiljett.events.controllers',
  'liubiljett.events.states'
]);

'use strict'

angular.module('liubiljett.events.controllers', [])

.controller('EventController', ['event', 'products',
  function (event, products) {
    var ctrl = this
    ctrl.event = event
    ctrl.event.products = products
  }
])

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

'use strict';

angular.module('liubiljett.home', [
  'liubiljett.home.states'
]);

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

'use strict'

angular.module('liubiljett.people', [
  'liubiljett.people.directives',
  'liubiljett.people.services',
  'liubiljett.people.states'
])

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

'use strict'

angular.module('liubiljett.people.services', [
  'restangular'
])

.factory('SessionService', ['$q', 'Raven', 'Restangular',
  function ($q, Raven, Restangular) {
    var currentCart
    var currentPerson

    function reloadCurrentPerson () {
      Restangular.one('people', 'current').get().then(
        function (person) {
          currentPerson = person
          Raven.setUserContext({
            'id': currentPerson.id,
            'email': currentPerson.email
          })
        })
    }

    function getCurrentPerson () {
      if (angular.isDefined(currentPerson)) {
        return $q.when(currentPerson)
      } else {
        return Restangular.one('people', 'current').get().then(
          function (person) {
            currentPerson = person
            Raven.setUserContext({
              'id': currentPerson.id,
              'email': currentPerson.email
            })
            return currentPerson
          },
          function (response) {
            if (response.status === 403) {
              currentPerson = null
              return currentPerson
            } else {
              console.error('Got a bad response from the server: ' + response)
            }
          })
      }
    }

    function getCurrentCart () {
      return getCurrentPerson().then(function (person) {
        return Restangular.oneUrl('carts', person.default_cart).get().then(
          function (cart) {
            currentCart = cart
            return currentCart
          })
      })
    }

    return {
      getCurrentCart: getCurrentCart,
      getCurrentPerson: getCurrentPerson,
      reloadCurrentPerson: reloadCurrentPerson
    }
  }])

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
              var url = $state.href($state.current.name, $state.current.params)
              if (url === null) {
                return '/'
              } else {
                return url
              }
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

'use strict'

angular.module('liubiljett.products', [
  'liubiljett.products.controllers',
  'liubiljett.products.directives',
  'liubiljett.products.models',
  'liubiljett.products.services',
  'liubiljett.products.states'
])

'use strict'

angular.module('liubiljett.products.controllers', [])

.controller('CartController', ['$scope', '$state', '$mdDialog', '$mdMedia',
  'Restangular', 'SessionService', 'Holding', 'stripe', 'cart',
  function ($scope, $state, $mdDialog, $mdMedia, Restangular, SessionService,
            Holding, stripe, cart) {
    var ctrl = this
    ctrl.cart = cart
    ctrl.cart.updateTotal()
    ctrl.card = {}
    ctrl.purchaseProgress = {
      status: null,
      statusMessage: ''
    }
    ctrl.purchaseProgressDialog = {
      autoWrap: false,
      clickOutsideToClose: false,
      controller: function () {
        this.hide = function () {
          $mdDialog.hide()
        }
        this.progress = ctrl.purchaseProgress
      },
      controllerAs: 'dialog',
      bindToController: true,
      templateUrl: StaticFile('liubiljett/products/templates/dialogs/purchaseProgressDialog.html')
    }
    ctrl.purchase = function () {
      ctrl.purchaseProgress.status = 'working'
      ctrl.purchaseProgress.statusMessage = null
      $mdDialog.show(ctrl.purchaseProgressDialog).then(function (response) {
        if (ctrl.purchaseProgress.status === 'succeeded') {
          SessionService.reloadCurrentPerson()
          $state.go('liubiljett.home')
        }
      })

      return stripe.card.createToken(ctrl.card)
        .then(function (response) {
          ctrl.purchaseProgress.status = 'working'
          return ctrl.cart.purchase(response.id)
        }, function (error) {
          ctrl.purchaseProgress.statusMessage = error.message
          ctrl.purchaseProgress.status = 'failed'
        })
        .then(function (purchasedCart) {
          ctrl.purchaseProgress.status = 'succeeded'
          return purchasedCart
        }, function (error) {
          ctrl.purchaseProgress.status = 'failed'
          ctrl.purchaseProgress.statusMessage = error.data.detail
        })
        .catch(function (err) {
          ctrl.purchaseProgress.status = 'failed'
          console.error('Other error occurred, possibly with your API', err.message)
        })
    }
    ctrl.deleteHolding = function (holding) {
      return Restangular.oneUrl('holdings', holding.url).remove().then(function (response) {
        return Restangular.oneUrl('carts', ctrl.cart.url).get()
      }).then(function (response) {
        ctrl.cart = response
        ctrl.cart.updateTotal()
      })
    }
  }
])

.controller('HoldingDetailController', ['holding',
  function (holding) {
    var ctrl = this
    ctrl.holding = holding
  }
])

.controller('ProductController', ['$state', '$mdToast', 'Money', 'SessionService', 'Holding',
  function ($state, $mdToast, Money, SessionService, Holding) {
    var ctrl = this
    ctrl.addToCart = function () {
      ctrl.product.addToCart().then(function (holding) {
        var toast = $mdToast.simple().content(ctrl.product.name + ' tillagd!').action('Gå till kundvagnen').highlightAction(false).position('bottom right').hideDelay(10000)
        return $mdToast.show(toast)
      }).then(function (response) {
        if (response === 'ok') {
          $state.go('liubiljett.cart')
        }
      })
    }

    SessionService.getCurrentPerson().then(function (person) {
      ctrl.loggedIn = (person !== null)
    })

    ctrl.product.updatePrice()
  }
])

.controller('UtilizeController', ['Holding',
  function (Holding) {
    var ctrl = this
    ctrl.holdings = null
    ctrl.loading = false
    ctrl.resetQueryParams = function () {
      ctrl.queryParams = {purchased: 'True'}
    }
    ctrl.resetQueryParams()

    ctrl.submit = function () {
      ctrl.loading = true

      Holding.getList(ctrl.queryParams).then(function (holdings) {
        ctrl.holdings = holdings
      }).finally(function (response) {
        ctrl.loading = false
        ctrl.resetQueryParams()
      })
    }
  }
])

'use strict';

angular.module('liubiljett.products.directives', [])

.directive('lbProductCard', [
  function () {
    return {
      scope: {},
      bindToController: {
        product: '='
      },
      controller: 'ProductController',
      controllerAs: 'ctrl',
      templateUrl: StaticFile('liubiljett/products/templates/directives/lb-product-card.html')
    }
  }
]);

'use strict'

angular.module('liubiljett.products.models', [])

.run(['Restangular', 'Money', 'Holding', 'SessionService',
  function (Restangular, Money, Holding, SessionService) {
    Restangular.extendModel('products', function (product) {
      product.variations.forEach(function (variation) {
        variation.selectedChoice = null
        variation.getSetSelectedChoice = function (newChoice) {
          // Note that newName can be undefined for two reasons:
          // 1. Because it is called as a getter and thus called with no arguments
          // 2. Because the property should actually be set to undefined. This happens e.g. if the
          //    input is invalid
          if (arguments.length) {
            variation.selectedChoice = newChoice
            product.updatePrice()
          }
          return variation.selectedChoice
        }
      })

      product.updatePrice = function () {
        var price = Money(product.base_price)
        product.modifiers.forEach(function (modifier) {
          price = price.plus(modifier.delta_amount)
        })
        product.variations.forEach(function (variation) {
          if (variation.selectedChoice !== null) {
            price = price.plus(variation.selectedChoice.delta_amount)
          }
        })

        product.price = price.toFixed(2)
      }

      product.addToCart = function () {
        return SessionService.getCurrentPerson().then(function (currentPerson) {
          var holding = {
            'cart': currentPerson.default_cart,
            'person': currentPerson.url,
            'product': product.url,
            'product_variation_choices': [],
            'quantity': 1
          }
          product.variations.forEach(function (variation) {
            holding.product_variation_choices.push(variation.selectedChoice.url)
          })
          return Holding.post(holding)
        })
      }

      return product
    })

    Restangular.extendModel('carts', function (cart) {
      cart.purchase = function (stripeToken) {
        return cart.one('purchase').patch({'stripe_token': stripeToken}).then(function (response) {
          return response
        })
      }

      cart.updateTotal = function () {
        var total = Money('0.00')
        cart.holdings.forEach(function (holding) {
          total = total.plus(holding.price)
        })
        cart.total = total.toFixed(2)
      }

      return cart
    })

    Restangular.extendModel('holdings', function (holding) {
      holding.utilize = function () {
        return holding.one('utilize').patch({}).then(function (response) {
          holding.utilized = response.utilized
        })
      }

      holding.unutilize = function () {
        return holding.one('unutilize').patch({}).then(function (response) {
          holding.utilized = response.utilized
        })
      }

      return holding
    })
  }
])

'use strict'

angular.module('liubiljett.products.services', [])

.factory('Holding', ['Restangular',
  function (Restangular) {
    return Restangular.service('holdings')
  }
])

'use strict'

angular.module('liubiljett.products.states', [])

.config(['$stateProvider',
  function ($stateProvider) {
    [
      {
        name: 'liubiljett.cart',
        url: 'cart/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/cart.main.html'),
            controller: 'CartController as ctrl'
          }
        },
        resolve: {
          cart: ['SessionService',
            function (SessionService) {
              return SessionService.getCurrentCart()
            }]
        }
      },
      {
        name: 'liubiljett.holding',
        abstract: true
      },
      {
        name: 'liubiljett.holding.detail',
        url: 'holdings/{holdingId}/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/holding.detail.main.html'),
            controller: 'HoldingDetailController as ctrl'
          }
        },
        resolve: {
          holding: ['$stateParams', 'Restangular',
            function ($stateParams, Restangular) {
              return Restangular.one('holdings', $stateParams.holdingId).get()
            }
          ]
        }
      },
      {
        name: 'liubiljett.holding.utilize',
        url: 'utilize/',
        views: {
          'main@': {
            templateUrl: StaticFile('liubiljett/products/templates/holding.utilize.main.html'),
            controller: 'UtilizeController as ctrl'
          }
        }
      }
    ].forEach($stateProvider.state)
  }
])
