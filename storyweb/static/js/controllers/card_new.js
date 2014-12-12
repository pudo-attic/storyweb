storyweb.controller('CardNewCtrl', ['$scope', '$routeParams', '$location', '$interval', '$http', 'cfpLoadingBar',
  function($scope, $routeParams, $location, $interval, $http, cfpLoadingBar) {
  $scope.card = {
    'title': '',
    'category': $location.search().category,
  };

  $scope.canSubmit = function() {
    return $scope.card.title && $scope.card.title.length > 1 && $scope.card.category;
  };

  $scope.saveCard = function () {
    cfpLoadingBar.start();
    $http.post('/api/1/cards', $scope.card).then(function(res) {
      cfpLoadingBar.complete();
      $location.path('/cards/' + res.data.id);
    });
  };

}]);
