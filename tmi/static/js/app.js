var storyweb = angular.module('storyweb', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'angular-loading-bar', 'contenteditable', 'truncate']);

storyweb.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 500;
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


storyweb.controller('StoryListCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
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
  $scope.story = {};
  $scope.cards = [];
  $scope.activeCards = 0;
  $scope.discardedCards = 0;
  $scope.tabs = {
    'pending': true
  };

  $scope.$on('pendingTab', function() {
    $scope.tabs.pending = true;
  });

  $http.get('/api/1/cards/' + $scope.cardId).then(function(res) {
    $scope.story = res.data;
    if (!$scope.story.text || !$scope.story.text.length) {
      $scope.story.text = 'Write your story here...<br><br>'
    }
  });

  $scope.$on('highlight', function(e, words) {
    realText = $scope.story.text;
    var regex = '(' + words.join('|') + ')';
    $scope.story.text = realText.replace(new RegExp(regex, 'gi'), function(t) {
      return '<span class="highlight">' + t + '</span>';
    });
  });

  $scope.$on('clearHighlight', function(e, words) {
    $scope.story.text = realText;
  });
//todo: update cards with links
  var updateCards = function() {
    if (initialLoad) {
      cfpLoadingBar.start();
    }
    $http.get('/api/1/cards/' + $scope.cardId + '/links', {ignoreLoadingBar: true}).then(function(res) {
      var newCards = [];
      angular.forEach(res.data.results, function(c) {
        var c = c.child;
        var exists = false;
        angular.forEach($scope.cards, function(o) {
          if (o['id'] == c['id']) {
            exists = true;
            o.references = c.references;
            o.wiki_text = c.wiki_text;
          }
        });
        if (!exists) newCards.push(c);
      });
      newCards = newCards.concat($scope.cards);
      newCards.sort(function(a, b) {
        if (a.offset == b.offset) {
          return a.updated_at.localeCompare(b.updated_at);
        }
        return a.offset - b.offset;
      });
      $scope.discardedCards = 0;
      $scope.activeCards = 0;

      angular.forEach(newCards, function(c) {
        c.discarded = c.status == 'discarded';
        if (c.discarded) {
          $scope.discardedCards++;
        } else {
          $scope.activeCards++;
        }
      });

      $scope.cards = newCards;
      if (initialLoad) {
        initialLoad = false;
        cfpLoadingBar.complete();
      }
    });
  };

  $interval(updateCards, 2000);

  $scope.saveStory = function () {
    cfpLoadingBar.start();
    $http.post('/api/1/cards/' + $scope.cardId, $scope.story).then(function(res) {
      console.log('Saved the story!');
      cfpLoadingBar.complete();
    });
  };

}]);

storyweb.directive('storywebCard', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '='
    },
    templateUrl: 'card.html',
    link: function (scope, element, attrs, model) {
      scope.mode = 'view';
      scope.expanded = false;

      var saveCard = function() {
        cfpLoadingBar.start();
        var url = '/api/cards/' + scope.story.id + '/links/' + scope.card.id;
        scope.card.discarded = scope.card.status == 'discarded';
        $http.post(url, scope.card).then(function(res) {
          scope.card = res.data;
          scope.card.discarded = scope.card.status == 'discarded';
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

      scope.toggleDiscarded = function() {
        if (scope.card.status == 'discarded') {
          scope.card.status = 'approved';
        } else {
          scope.card.status = 'discarded';
        }
        saveCard();
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
        return scope.card.references.length > 0;
      };

      scope.hasWiki = function() {
        if(scope.card.wiki_text != undefined){
          return scope.card.wiki_text.length > 0;
        }else{
          return false;
        }
      };

      scope.hasCustom = function() {
        return scope.card.text.length > 0;
      };

      scope.hasAliases = function() {
        return scope.card.aliases.length > 1;
      };
    }
  };
}]);


storyweb.directive('storywebNewCard', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '='
    },
    templateUrl: 'card_new.html',
    link: function (scope, element, attrs, model) {
      scope.card = {'score': 100, 'category': 'Company'};
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
// todo: score?
        scope.card = {'score': 100, 'category': 'Company'};
        $http.post('/api/1/cards', card).then(function(res) {
          var child = {'child': res.data.id };
          // link to story
          var url = '/api/1/cards/' + scope.story.id + '/links';
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
    templateUrl: 'story_list.html',
    controller: 'StoryListCtrl'
  });

  $routeProvider.when('/cards/:id', {
    templateUrl: 'story.html',
    controller: 'CardCtrl'
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $locationProvider.html5Mode(false);
}]);
