// FOUNDATION FOR APPS TEMPLATE GULPFILE
// -------------------------------------
// This file processes all of the assets in the "client" folder, combines them with the Foundation for Apps assets, and outputs the finished files in the "build" folder as a finished app.

// 1. LIBRARIES
// - - - - - - - - - - - - - - -

var $ = require('gulp-load-plugins')()
var argv = require('yargs').argv
var gulp = require('gulp')
var rimraf = require('rimraf')
var router = require('front-router')
var sequence = require('run-sequence')

// Check for --production flag
var isProduction = !!(argv.production)

// 2. FILE PATHS
// - - - - - - - - - - - - - - -

var paths = {
  assets: [
    './tickle/static-src/**/*.*',
    '!./tickle/static-src/templates/**/*.*',
    '!./tickle/static-src/assets/{scss,js}/**/*.*'
  ],
  // Sass will check these folders for files when you use @import.
  sass: [
    'tickle/static-src/assets/scss',
    'node_modules/foundation-apps/scss'
  ],
  // These files include Foundation for Apps and its dependencies
  foundationJS: [
    'node_modules/fastclick/lib/fastclick.js',
    'node_modules/viewport-units-buggyfill/viewport-units-buggyfill.js',
    'node_modules/tether/tether.js',
    'node_modules/hammerjs/hammer.js',
    'node_modules/angular/angular.js',
    'node_modules/angular-animate/angular-animate.js',
    'node_modules/angular-ui-router/release/angular-ui-router.js',
    'node_modules/foundation-apps/js/vendor/**/*.js',
    'node_modules/foundation-apps/js/angular/**/*.js',
    '!node_modules/foundation-apps/js/angular/app.js'
  ],
  // These files are for your app's JavaScript
  appJS: [
    'tickle/static-src/assets/js/**/*.js'
  ]
}

// 3. TASKS
// - - - - - - - - - - - - - - -

// Cleans the build directory
gulp.task('clean', function (cb) {
  rimraf('./tickle/static', cb)
})

// Copies everything in the client folder except templates, Sass, and JS
gulp.task('copy', function () {
  return gulp.src(paths.assets, {
    base: './tickle/static-src/'
  })
    .pipe(gulp.dest('./tickle/static'))
})

// Copies your app's page templates and generates URLs for them
gulp.task('copy:templates', function (cb) {
  gulp.src('./tickle/static-src/templates/**/*.html')
    .pipe(router({
      path: 'tickle/static/assets/js/routes.js',
      root: 'tickle/static-src'
    }))
    .pipe(gulp.dest('./tickle/static/templates'))

  gulp.src('tickle/static-src/templates/**/*.html')
    .pipe($.minifyHtml({
      empty: true,
      spare: true,
      quotes: true
    }))
    .pipe($.ngHtml2js({
      prefix: '/static/templates/',
      moduleName: 'tickle',
      declareModule: false
    }))
    .pipe($.uglify())
    .pipe($.concat('templates.js'))
    .pipe(gulp.dest('./tickle/static/assets/js'))

  cb()
})

// Compiles the Foundation for Apps directive partials into a single JavaScript file
gulp.task('copy:foundation', function (cb) {
  gulp.src('node_modules/foundation-apps/js/angular/components/**/*.html')
    .pipe($.minifyHtml({
      empty: true,
      spare: true,
      quotes: true
    }))
    .pipe($.ngHtml2js({
      prefix: 'components/',
      moduleName: 'foundation',
      declareModule: false
    }))
    .pipe($.uglify())
    .pipe($.concat('foundation-templates.js'))
    .pipe(gulp.dest('./tickle/static/assets/js'))

  // Iconic SVG icons
  gulp.src('./node_modules/foundation-apps/iconic/**/*')
    .pipe(gulp.dest('./tickle/static/assets/img/iconic/'))
  cb()
})

// Compiles Sass
gulp.task('sass', function () {
  var minifyCss = $.if(isProduction, $.minifyCss())

  return gulp.src('tickle/static-src/assets/scss/app.scss')
    .pipe($.sass({
      includePaths: paths.sass,
      outputStyle: (isProduction ? 'compressed' : 'nested'),
      errLogToConsole: true
    }))
    .pipe($.autoprefixer({
      browsers: ['last 2 versions', 'ie 10']
    }))
    .pipe(minifyCss)
    .pipe(gulp.dest('./tickle/static/assets/css/'))
})

// Compiles and copies the Foundation for Apps JavaScript, as well as your app's custom JS
gulp.task('uglify', ['uglify:foundation', 'uglify:app'])

gulp.task('uglify:foundation', function (cb) {
  var uglify = $.if(isProduction, $.uglify()
    .on('error', function (e) {
      console.log(e)
    }))

  return gulp.src(paths.foundationJS)
    .pipe(uglify)
    .pipe($.concat('foundation.js'))
    .pipe(gulp.dest('./tickle/static/assets/js/'))
})

gulp.task('uglify:app', function () {
  var uglify = $.if(isProduction, $.uglify()
    .on('error', function (e) {
      console.log(e)
    }))

  return gulp.src(paths.appJS)
    .pipe(uglify)
    .pipe($.concat('app.js'))
    .pipe(gulp.dest('./tickle/static/assets/js/'))
})

// Starts a test server, which you can view at http://localhost:8079
gulp.task('server', ['build'], function () {
  gulp.src('./build')
    .pipe($.webserver({
      port: 8079,
      host: 'localhost',
      fallback: 'index.html',
      livereload: true,
      open: true
    }))
})

// Builds your entire app once, without starting a server
gulp.task('build', function (cb) {
  sequence('clean', ['copy', 'copy:foundation', 'sass', 'uglify'], 'copy:templates', cb)
})

// Default task: builds your app, starts a server, and recompiles assets when they change
gulp.task('default', ['server'], function () {
  // Watch Sass
  gulp.watch(['./tickle/static-src/assets/scss/**/*', './scss/**/*'], ['sass'])

  // Watch JavaScript
  gulp.watch(['./tickle/static-src/assets/js/**/*', './js/**/*'], ['uglify:app'])

  // Watch static files
  gulp.watch(['./tickle/static-src/**/*.*', '!./tickle/static-src/templates/**/*.*', '!./tickle/static-src/assets/{scss,js}/**/*.*'], ['copy'])

  // Watch app templates
  gulp.watch(['./tickle/static-src/templates/**/*.html'], ['copy:templates'])
})
