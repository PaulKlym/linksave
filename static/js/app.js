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
        .when('/contact', {
            templateUrl: '/static/views/links/contact.html'})
        .otherwise({ redirectTo: '/'});
}]);

app.service('MainService', function($cookies, $rootScope) {
    this.isLogin = function(scope) {
        console.log($cookies.token)
        var is = $cookies.token != undefined;
        if (is && scope != undefined && scope.user != undefined) $rootScope.isLogin = 'hi ' + scope.user.nick;
        return is;
    }
});

app.controller('RegisterController',
               ['$scope', '$http', '$location', 'MainService',
                function($scope, $http, $location, MainService) {
                    MainService.isLogin($scope);
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
               ['$scope', '$http', '$location', '$cookies', 'MainService',
                function($scope, $http, $location, $cookies, MainService) {
                    MainService.isLogin($scope);
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
               ['$scope', '$http', '$location', '$cookies', 'MainService',
                function($scope, $http, $location, $cookies, MainService) {
                    $http.get("/api/v1.0/logout?token=" + $cookies.token)
                        .success(function(data, status, headers, config) {
                            $cookies.token = undefined;
                            $scope.user = undefined;
                            $scope.links = undefined;
                            $location.path("/login");
                            MainService.isLogin();
                        }).error(function(data, status, headers, config) {
                            $cookies.token = undefined;
                            $location.path("/login");
                            MainService.isLogin();
                        });

               }]);


app.controller('MainController',
               ['$scope', '$http', '$location', '$cookies', 'MainService',
                function($scope, $http, $location, $cookies, MainService) {

                    if (MainService.isLogin()) {
                    } else {
                        $location.path('/login');
                        return;
                    }
                    
                    if ($scope.user == undefined) {
                    $http.get('/api/v1.0/user?token=' + $cookies.token)
                            .success(function(data, status, headers, config) {
                                $scope.user = data;
                                MainService.isLogin($scope);

                        }).error(function(data, status, headers, config) {
                            if (status == 403) {
                                $location.path("/login");
                                MainService.isLogin();
                                return
                            }
                            $scope.error = data;
                        });
                    }
                    
                    document.getElementById("linkField").focus();
                    $scope.offset = 0;

                    $scope.dataLoading = false;
                    $scope.update = function(offset) {
                        $http.get("/api/v1.0/links?token=" + $cookies.token + "&offset=" + offset )
                        .success(function(data, status, headers, config) {
                            $scope.links = data;
                        }).error(function(data, status, headers, config) {
                            if (status == 403) {
                                $location.path("/login");
                                return
                            }
                            $scope.error = data;
                        });
                    }

                    
                    $scope.update($scope.offset)
                    $scope.loaded = true;




                    var limit = 4;                    
                    $scope.next = function() {
                        $scope.offset = $scope.offset + $scope.links.length;
                        if ($scope.offset >= limit) {
                            $scope.isPrev = true;
                        }
                        $scope.update($scope.offset)
                        if ($scope.links.length < limit) {
                            $scope.isNext = false;
                        }
                    }
                    $scope.prev = function() {
                        $scope.offset = $scope.offset - limit;
                        if ($scope.offset <= 0) {
                            $scope.offset = 0;
                            $scope.isPrev = false;
                        }
                        $scope.update($scope.offset);
                    }
                    $scope.isNext = true
                    $scope.isPrev = false




                    
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
                        l = $.trim(l)
                        if (l == '' || l == undefined || l == null)
                            return
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

$(window).focus(function() {
    var e = document.getElementById("linkField");
    e.focus();
    e.select();
});

