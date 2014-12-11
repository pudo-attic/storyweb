storyweb.controller('CardCtrl', ['$scope', '$routeParams', '$location', '$interval', '$http', 'cfpLoadingBar',
  function($scope, $routeParams, $location, $interval, $http, cfpLoadingBar) {
  var initialLoad = true,
      realText = null;

  $scope.cardId = $routeParams.id;
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

  //todo: update cards with links
  var updateLinks = function() {
    if (initialLoad) {
      cfpLoadingBar.start();
    }
    $http.get('/api/1/cards/' + $scope.cardId + '/links', {ignoreLoadingBar: true}).then(function(res) {
      var newLinks = [];
      angular.forEach(res.data.results, function(c) {
        var exists = false;
        angular.forEach($scope.links, function(o) {
          if (o['id'] == c['id']) {
            exists = true;
            o.child.references = c.child.references;
          }
        });
        if (!exists) newLinks.push(c);
      });
      newLinks = newLinks.concat($scope.links);
      newLinks.sort(function(a, b) {
        if (a.offset == b.offset) {
          return a.updated_at.localeCompare(b.updated_at);
        }
        return a.offset - b.offset;
      });
      $scope.rejectedLinks = 0;
      $scope.activeLinks = 0;

      angular.forEach(newLinks, function(l) {
        l.rejected = l.status == 'rejected';
        if (l.rejected) {
          $scope.rejectedLinks++;
        } else {
          $scope.activeLinks++;
        }
      });

      $scope.links = newLinks;
      if (initialLoad) {
        initialLoad = false;
        cfpLoadingBar.complete();
      }
    });
  };

  $interval(updateLinks, 2000);

  $scope.saveCard = function () {
    cfpLoadingBar.start();
    $http.post('/api/1/cards/' + $scope.cardId, $scope.card).then(function(res) {
      cfpLoadingBar.complete();
    });
  };

}]);
