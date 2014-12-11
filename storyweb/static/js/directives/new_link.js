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
