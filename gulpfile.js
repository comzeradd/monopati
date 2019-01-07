/* global require */

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
var gulpFilter = require('gulp-filter');
var eslint = require('gulp-eslint');
var stylelint = require('gulp-stylelint');

var lintPathsJS = [
    'skel/static/js/*.js',
    'gulpfile.js'
];

var lintPathsCSS = [
    'skel/static/css/*.css'
];

gulp.task('js:lint', () => {
    return gulp.src(lintPathsJS)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('css:lint', () => {
    return gulp.src(lintPathsCSS)
        .pipe(stylelint({
            reporters: [{ formatter: 'string', console: true}]
        }));
});

gulp.task('assets', () => {
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
        .pipe(gulp.dest('skel/static/lib'));
});

gulp.task('test', (done) => {
    gulp.parallel('js:lint');
    gulp.parallel('css:lint');
    done();
});

gulp.task('default', (done) => {
    gulp.series('assets');
    gulp.series('test');
    done();
});
