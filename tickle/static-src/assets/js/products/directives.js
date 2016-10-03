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
