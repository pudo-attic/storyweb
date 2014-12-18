storyweb.controller('SearchCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  $scope.search = $location.search();
  $scope.result = {'results': []};

  $scope.loadPage = function(page) {
    $location.search('offset', $scope.result.limit * (page-1));
  };

  $http.get('/api/1/cards/_search', {'params': $scope.search}).then(function(res) {
      $scope.result = res.data;
      $scope.result.end = Math.min($scope.result.total, $scope.result.offset + $scope.result.limit);
    });  
}]);
