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
