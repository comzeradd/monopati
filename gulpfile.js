/* global require, exports */

const gulp = require('gulp');
const uglify = require('gulp-uglify');
const cleanCSS = require('gulp-clean-css');
const gulpFilter = require('gulp-filter');
const eslint = require('gulp-eslint');
const stylelint = require('gulp-stylelint');

const lintPathsJS = [
    'skel/static/js/*.js',
    'gulpfile.js'
];

const lintPathsCSS = [
    'skel/static/css/*.css'
];

function lint_js() {
    return gulp.src(lintPathsJS)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
}

function lint_css() {
    return gulp.src(lintPathsCSS)
        .pipe(stylelint({
            reporters: [{ formatter: 'string', console: true}]
        }));
}

function assets() {
    var filterJS = gulpFilter('**/*.js', { restore: true });
    var filterCSS = gulpFilter('**/*.css', { restore: true });
    var p = require('./package.json');
    var assets = p.assets;
    return gulp.src(assets, {cwd : 'node_modules/**'})
        .pipe(filterJS)
        .pipe(uglify())
        .pipe(filterJS.restore)
        .pipe(filterCSS)
        .pipe(cleanCSS({rebase: false}))
        .pipe(filterCSS.restore)
        .pipe(gulp.dest('monopati/skel/static/lib'));
}

exports.test = gulp.parallel(lint_css, lint_js);
exports.default = gulp.series(lint_css, lint_js, assets);
