var storyweb = angular.module('storyweb', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'angular-loading-bar', 'contenteditable', 'truncate']);

storyweb.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 100;
}]);

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

storyweb.directive('storywebLink', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'parent': '=',
      'link': '='
    },
    templateUrl: 'link.html',
    link: function (scope, element, attrs, model) {
      scope.mode = 'view';
      scope.card = {};
      scope.expanded = false;

      scope.$watch('link', function(l) {
        if (l) scope.card = l.child;
      });

      var saveCard = function() {
        cfpLoadingBar.start();
        var url = '/api/1/cards/' + scope.card.id;
        $http.post(url, scope.card).then(function(res) {
          scope.card = res.data;
          cfpLoadingBar.complete();
        });
      };

      var saveLink = function() {
        cfpLoadingBar.start();
        var url = '/api/1/cards/' + scope.parent.id + '/links/' + scope.link.id;
        scope.link.rejected = scope.link.status == 'rejected';
        $http.post(url, scope.link).then(function(res) {
          scope.link = res.data;
          scope.link.rejected = scope.link.status == 'rejected';
          cfpLoadingBar.complete();
        });
      };

      scope.mouseIn = function() {
        scope.$emit('highlight', scope.card.aliases);
      };

      scope.mouseOut = function() {
        scope.$emit('clearHighlight');
      };

      scope.toggleMode = function() {
        if (scope.editMode()) {
          saveCard();
        }
        scope.mode = scope.mode == 'view' ? 'edit' : 'view';
      };

      scope.toggleRejected = function() {
        if (scope.link.status == 'rejected') {
          scope.link.status = 'approved';
        } else {
          scope.link.status = 'rejected';
        }
        saveLink();
      };

      scope.expandCard = function() {
        scope.expanded = !scope.expanded;
      };

      scope.editMode = function() {
        return scope.mode == 'edit';
      };

      scope.viewMode = function() {
        return scope.mode == 'view';
      };

      scope.hasReferences = function() {
        return scope.card.references && scope.card.references.length > 0;
      };

      scope.hasText = function() {
        return scope.card.text && scope.card.text.length > 0;
      };

      scope.hasAliases = function() {
        return scope.card.aliases && scope.card.aliases.length > 1;
      };
    }
  };
}]);


storyweb.directive('storywebNewLink', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'parent': '='
    },
    templateUrl: 'link_new.html',
    link: function (scope, element, attrs, model) {
      scope.card = {'category': 'Company'};
      scope.categoryOptions = ["Company", "Person", "Organization"];

      scope.selectCategory = function(index) {
        scope.card.category = scope.categoryOptions[index];
      };

      scope.canSubmit = function() {
        return scope.card.title && scope.card.title.length > 1;
      };

      scope.saveCard = function() {
        if (!scope.canSubmit()) return;
        cfpLoadingBar.start();
        var card = angular.copy(scope.card);
        // create new card
        scope.card = {'category': 'Company'};
        $http.post('/api/1/cards', card).then(function(res) {
          var child = {
            'child': res.data.id,
            'status': 'approved',
            'offset': 0
          };
          // link to story
          var url = '/api/1/cards/' + scope.parent.id + '/links';
          scope.$emit('pendingTab');
          $http.post(url, child).then(function(res) {
            scope.card = res.data;
            cfpLoadingBar.complete();
          });
        });

      };

    }
  };
}]);

storyweb.directive('storywebReference', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '=',
      'reference': '='
    },
    templateUrl: 'reference.html',
    link: function (scope, element, attrs, model) {

    }
  };
}]);


storyweb.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {

  $routeProvider.when('/', {
    templateUrl: 'article_list.html',
    controller: 'ArticleListCtrl'
  });

  $routeProvider.when('/cards/:id', {
    templateUrl: 'card.html',
    controller: 'CardCtrl'
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $locationProvider.html5Mode(false);
}]);
