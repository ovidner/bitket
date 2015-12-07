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
