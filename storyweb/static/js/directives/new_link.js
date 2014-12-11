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

      scope.suggestCard = function(q) {
        console.log(q);
        var params = {'prefix': q};
        return $http.get('/api/1/cards/_suggest', {'params': params}).then(function(res) {
          return res.data.options;
        });
      };

      scope.linkCard = function(card) {
        saveLink(card);
      };

      scope.saveCard = function() {
        if (!scope.canSubmit()) return;
        cfpLoadingBar.start();
        var card = angular.copy(scope.card);
        // create new card
        $http.post('/api/1/cards', card).then(function(res) {
          saveLink(res.data);
        });

        scope.card = {'category': 'Company'};
      };

      var saveLink = function(child) {
        var link = {
          'child': child,
          'status': 'approved',
          'offset': 0
        };
        var url = '/api/1/cards/' + scope.parent.id + '/links';
        $http.post(url, link).then(function(res) {
          cfpLoadingBar.complete();
        });
        scope.$emit('pendingTab');
      };
    }
  };
}]);
