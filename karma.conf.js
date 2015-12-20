// Karma configuration
// Generated on Mon Nov 30 2015 21:11:38 GMT-0800 (PST)

module.exports = function(config) {
    config.set({

        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '',


        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            "dashboard/static/vendor/angular/angular.js",
            "dashboard/static/vendor/d3/d3.js",
            "dashboard/static/vendor/c3/c3.js",
            "dashboard/static/vendor/angular-mocks/angular-mocks.js",
            "dashboard/static/vendor/angular-ui-router/release/angular-ui-router.min.js",
            "dashboard/static/vendor/angular-bootstrap/ui-bootstrap-tpls.min.js",
            "dashboard/static/vendor/angular-sanitize/angular-sanitize.js",
            "dashboard/static/vendor/Chart.js/Chart.min.js",
            "dashboard/static/vendor/ui-select/dist/select.js",
            "dashboard/static/vendor/angular-chart.js/dist/angular-chart.js",
            "dashboard/static/vendor/lodash/lodash.min.js",
            "dashboard/static/vendor/checklist-model/checklist-model.js",
            "dashboard/static/vendor/angular-chart/angular-chart.js",
            "dashboard/static/vendor/ng-table/dist/ng-table.js",
            "dashboard/static/js/**/*.js"
        ],


        // list of files to exclude
        exclude: [],


        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {},


        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['progress'],


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['Chrome'],


        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true,

        // Concurrency level
        // how many browser should be started simultanous
        concurrency: Infinity
    })
}