storyweb.controller('AppCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  $scope.session = {'logged_in': false, 'is_admin': false};
  $http.get('/api/1/session').then(function(res) {
    $scope.session = res.data;
    if (!$scope.session.logged_in) {
      document.location.href = '/';
    }
  });

  $scope.newStory = function() {
    cfpLoadingBar.start();
    var empty = {'title': '', 'text': '', 'category': 'Article'};
    $http.post('/api/1/cards', empty).then(function(res) {
      $location.path('/cards/' + res.data.id);
      cfpLoadingBar.complete();
    });
  };

}]);
