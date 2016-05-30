var app = angular.module('linksave', ['ngResource', 'ngCookies']);


app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/login', {
            templateUrl: '/static/views/links/login.html',
            controller: 'LoginController'})
        .when('/logout', {
            templateUrl: '/static/views/links/logout.html',
            controller: 'LogoutController'})
        .when('/register', {
            templateUrl: '/static/views/links/register.html',
            controller: 'RegisterController'})
        .when('/', {
            templateUrl: '/static/views/links/list.html',
            controller: 'MainController'})
        .when('/about', {
            templateUrl: '/static/views/links/about.html'})
        .when('/forget', {
            templateUrl: '/static/views/links/forget.html'})
        .when('/settings', {
            templateUrl: '/static/views/links/settings.html'})
        .otherwise({ redirectTo: '/'});
}]);

app.controller('RegisterController',
               ['$scope', '$http', '$location', '$cookies',
                function($scope, $http, $location, $cookies) {
                    $scope.register = function(user) {
                        
                       $http.post("/api/v1.0/register", user)
                           .success(function(data, status, headers, config) {
                               $location.path("/login");
                           }).error(function(data, status, headers, config) {
                                $scope.error = data;
                           });
                   }
               }]);


app.controller('LoginController',
               ['$scope', '$http', '$location', '$cookies', '$rootScope',
                function($scope, $http, $location, $cookies, $rootScope) {
                    // $rootScope.isLogin = 'Login';
                    $scope.login = function(user) {
                       $http.post("/api/v1.0/login", user)
                           .success(function(data, status, headers, config) {
                               $cookies.token = data['token']
                               $location.path("/");
                               
                           }).error(function(data, status, headers, config) {
                               if (status == 403) {
                                   $location.path("/login");
                                   return
                               }
                               $scope.error = data;
                           });
                   }
               }]);

app.controller('LogoutController',
               ['$scope', '$http', '$location', '$cookies', '$rootScope',
                function($scope, $http, $location, $cookies, $rootScope) {
                    $rootScope.isLogin = 'Login';

                    $http.get("/api/v1.0/logout?token=" + $cookies.token)
                        .success(function(data, status, headers, config) {
                            $cookies.token = '';
                            $location.path("/login");
                        }).error(function(data, status, headers, config) {
                            $cookies.token = '';
                            $location.path("/login");
                        });
               }]);


app.controller('MainController',
               ['$scope', '$http', '$location', '$cookies', '$rootScope',
                function($scope, $http, $location, $cookies, $rootScope) {
                    if ($scope.user == undefined) {
                    $http.get('/api/v1.0/user?token=' + $cookies.token)
                        .success(function(data, status, headers, config) {
                            $scope.user = data;
                        }).error(function(data, status, headers, config) {
                            $scope.error = data;
                        });
                    }
                    
                    document.getElementById("linkField").focus();

                    $rootScope.isLogin = 'Logout';

                    $scope.dataLoading = false;
                    $http.get("/api/v1.0/links?token=" + $cookies.token)
                        .success(function(data, status, headers, config) {
                            $scope.links = data;
                        }).error(function(data, status, headers, config) {
                            if (status == 403) {
                                $location.path("/login");
                                return
                            }
                            $scope.error = data;
                        });

                    $scope.del = function(i) {
                        $http.delete("/api/v1.0/links/" + $scope.links[i]['_id']['$oid'] + "?token=" + $cookies.token)
                            .success(function(data, status, headers, config) {
                            $scope.links.splice(i, 1)
                        }).error(function(data, status, headers, config) {
                            $scope.error = data
                        });
                   }

                    $scope.add = function(l) {
                        if ($scope.dataLoading) return;
                        $scope.dataLoading = true;
                        $http.post("/api/v1.0/links?token=" + $cookies.token, {link: l})
                            .success(function(data, status, headers, config) {
                                $scope.links.unshift(data)
                                $scope.dataLoading = false;

                            }).error(function(data, status, headers, config) {
                               $scope.error = data;
                               $scope.dataLoading = false;
                           });
                       $scope.link = ''
                   };
               }]);
