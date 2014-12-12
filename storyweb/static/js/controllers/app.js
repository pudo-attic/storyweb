
storyweb.controller('AppCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  $scope.searchQuery = '';
  $scope.session = {'logged_in': false, 'is_admin': false};
  
  $scope.search = function() {
    $location.search('q', $scope.searchQuery);
    $location.path('/search');
  };

  $scope.$on('$locationChangeSuccess', function(event) {
    $scope.searchQuery = $location.search().q || '';
  });

  $scope.searchGo = function($item) {
    $location.search('q', null);
    $location.path('/cards/' + $item.id);
  };

  $scope.suggestCard = function(q) {
    var params = {'prefix': q};
    return $http.get('/api/1/cards/_suggest', {'params': params}).then(function(res) {
      return res.data.options;
    });
  };

  $http.get('/api/1/session').then(function(res) {
    $scope.session = res.data;
    if (!$scope.session.logged_in) {
      document.location.href = '/';
    }
  });

}]);
