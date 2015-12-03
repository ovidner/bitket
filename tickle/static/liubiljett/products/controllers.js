'use strict'

angular.module('liubiljett.products.controllers', [])

.controller('CartController', ['$scope', '$mdDialog', '$mdMedia', 'stripe', 'cart',
  function ($scope, $mdDialog, $mdMedia, stripe, cart) {
    var ctrl = this
    ctrl.cart = cart
    ctrl.card = {}
    ctrl.purchaseProgress = {
      status: null,
      statusMessage: ''
    }
    ctrl.purchaseProgressDialog = {
      autoWrap: false,
      clickOutsideToClose: false,
      controller: function () {
        console.log(this)
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
      $mdDialog.show(ctrl.purchaseProgressDialog)

      return stripe.card.createToken(ctrl.card)
        .then(function (response) {
          ctrl.purchaseProgress.status = 'working'
          return ctrl.cart.purchase(response.id)
        }, function (error) {
          ctrl.purchaseProgress.status = 'failed'
          ctrl.purchaseProgress.statusMessage = error.message
        })
        .then(function (purchasedCart) {
          ctrl.purchaseProgress.status = 'succeeded'
          $mdDialog.hide(ctrl.purchaseProgressDialog)
          return purchasedCart
        }, function (error) {
          ctrl.purchaseProgress.status = 'failed'
          ctrl.purchaseProgress.statusMessage = error.data.detail
          console.log(error.message)
          console.log(error.data)
        })
        .catch(function (err) {
          ctrl.purchaseProgress.status = 'failed'
          console.log(err)
          console.error('Other error occurred, possibly with your API', err.message)
        })
    }
  }
])

.controller('ProductController', ['Money', 'SessionService', 'Holding',
  function (Money, SessionService, Holding) {
    var ctrl = this
    ctrl.product.updatePrice()
  }
])
