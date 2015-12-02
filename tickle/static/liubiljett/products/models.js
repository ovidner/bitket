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
        SessionService.getCurrentPerson().then(function (currentPerson) {
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
          Holding.post(holding)
        })
      }

      return product
    })
  }
])
