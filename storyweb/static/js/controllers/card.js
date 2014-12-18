storyweb.controller('CardCtrl', ['$scope', '$routeParams', '$location', '$interval', '$http', 'cfpLoadingBar',
  function($scope, $routeParams, $location, $interval, $http, cfpLoadingBar) {
  var refreshSince = null,
      realText = null;

  $scope.cardId = $routeParams.id;
  $scope.updatesPending = false;
  $scope.card = {};
  $scope.links = [];
  $scope.activeLinks = 0;
  $scope.rejectedLinks = 0;
  $scope.tabs = {
    'pending': true
  };

  $scope.$on('pendingTab', function() {
    $scope.tabs.pending = true;
  });

  $http.get('/api/1/cards/' + $scope.cardId).then(function(res) {
    $scope.card = res.data;
    if (!$scope.card.text || !$scope.card.text.length) {
      $scope.card.text = 'Write your story here...<br><br>'
    }
  });

  $scope.$on('highlight', function(e, words) {
    realText = $scope.card.text;
    var regex = '(' + words.join('|') + ')';
    $scope.card.text = realText.replace(new RegExp(regex, 'gi'), function(t) {
      return '<span class="highlight">' + t + '</span>';
    });
  });

  $scope.$on('clearHighlight', function(e, words) {
    $scope.card.text = realText;
  });

  $scope.$on('linkChange', function() {
    console.log("LINK CHANGE");
    $scope.updateLinks();
  });

  $scope.updateLinks = function() {
    $scope.updatesPending = false;
    refreshSince = new Date();
    cfpLoadingBar.start();
    $http.get('/api/1/cards/' + $scope.cardId + '/links').then(function(res) {
      $scope.rejectedLinks = 0;
      $scope.activeLinks = 0;

      angular.forEach(res.data.results, function(link) {
        if (link.rejected) {
          $scope.rejectedLinks++;
        } else {
          $scope.activeLinks++;
        }
      });

      $scope.links = res.data.results;
      cfpLoadingBar.complete();
    });
  };

  var checkRefresh = function() {
    if (!refreshSince) return;
    var params = {'since': refreshSince.toISOString()},
        url = $scope.card.api_url + '/links/_refresh';
    $http.get(url, {'params': params}).then(function(res) {
      if (res.data.updated.length == 0) {
        $scope.updatesPending = false;
      } else {
        $scope.updatesPending = res.data.updated;
      }
    });
  }

  $scope.saveCard = function () {
    cfpLoadingBar.start();
    $http.post('/api/1/cards/' + $scope.cardId, $scope.card).then(function(res) {
      cfpLoadingBar.complete();
    });
  };

  $scope.updateLinks();
  var refreshInterval = $interval(checkRefresh, 2000);
  $scope.$on('$destroy', function() {
    $interval.cancel(refreshInterval);
  });

}]);
