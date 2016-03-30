var gulp = require('gulp');
var concat = require('gulp-concat');
var templateCache = require('gulp-angular-templatecache');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

var node_modules = "node_modules";
var node_modules_js = [
    node_modules + "/angular/angular.js",
    node_modules + "/angular-animate/angular-animate.js",
    node_modules + "/angular-aria/angular-aria.js",
    node_modules + "/angular-material/angular-material.js",
    node_modules + "/angular-messages/angular-messages.js",
];
var node_modules_css = [
    node_modules + "/angular-material/angular-material.css"
];

// PATHS
var app = 'app';
var app_js = [app + '/**/*.js', "!" + app + '/templates.js'];
var app_html = app + '/**/*.html';
var app_scss = app + '/app.scss';
var app_module_scss = app + '/**/*.scss';

var dist = "similarity/static/similarity";
var vendor_js = "vendor.js";
var vendor_css = "vendor.css";
var js = "index.js";
var css = "index.css";

// Vendor JS
gulp.task('vendor-js', function() {
    gulp.src(node_modules_js)
    .pipe(concat(vendor_js))
    .pipe(gulp.dest(dist));
});
// Vendor CSS
gulp.task('vendor-css', function() {
    gulp.src(node_modules_css)
    .pipe(concat(vendor_css))
    .pipe(gulp.dest(dist));
});

// Templates
gulp.task('templates', function () {
    gulp.src(app_html)
    .pipe(templateCache({'standalone':1}))
    .pipe(gulp.dest(dist));
});
// JS
gulp.task('js', function() {
    return gulp.src(app_js)
        .pipe(concat(js))
        .pipe(gulp.dest(dist));
});
// SASS
gulp.task('sass', function() {
    gulp.src(app_scss)
    .pipe(sass())
    .pipe(autoprefixer({
        browsers: ['last 2 versions'],
    }))
    .pipe(concat(css))
    .pipe(gulp.dest(dist));
});

// Watch
gulp.task('watch', function() {
    gulp.watch(node_modules_js, ['vendor-js']);
    gulp.watch(node_modules_css, ['vendor-css']);
    gulp.watch(app_js, ['js']);
    gulp.watch(app_scss, ['sass']);
});

// Default
gulp.task('default', ['vendor-js', 'vendor-css', 'templates', 'js', 'sass', 'watch'])
gulp.task('build',   ['vendor-js', 'vendor-css', 'templates', 'js', 'sass'])
