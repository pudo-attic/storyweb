storyweb.controller('SearchCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  var search = $location.search();
  $scope.result = {'results': []};


  $http.get('/api/1/cards/_search', search).then(function(res) {
    $scope.result = res.data;
  });

}]);

