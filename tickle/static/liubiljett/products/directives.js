'use strict';

angular.module('liubiljett.products.directives', [])

.directive('lbProductCard', [
  function () {
    return {
      scope: {
        product: '='
      },
      templateUrl: StaticFile('liubiljett/products/templates/directives/lb-product-card.html')
    }
  }
]);
