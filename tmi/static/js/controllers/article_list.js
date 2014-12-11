storyweb.controller('ArticleListCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  $scope.stories = [];

  cfpLoadingBar.start();
  var params = {'category': 'Article'};
  $http.get('/api/1/cards', {params: params}).then(function(res) {
    $scope.stories = res.data.results;
    cfpLoadingBar.complete();
  });

}]);

