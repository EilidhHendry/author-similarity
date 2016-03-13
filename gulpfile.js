var gulp = require('gulp');
var concat = require('gulp-concat');

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

var vendor_js = "vendor.js";
var vendor_css = "vendor.css";
var dist = "similarity/static/similarity";

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

// Watch
gulp.task('watch', function() {
    gulp.watch(node_modules_js, ['vendor-js']);
    gulp.watch(node_modules_css, ['vendor-css']);
});

// Default
gulp.task('default', ['vendor-js', 'vendor-css', 'watch']);
gulp.task('build', ['vendor-js', 'vendor-css']);
