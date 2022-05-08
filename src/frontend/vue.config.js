const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:8080/"
  // publicPath: "/static",
  outputDir: "../dist",
  assetsDir: "./static",
  productionSourceMap: false,

  // Webpack config, reference: https://cli.vuejs.org/guide/webpack.html
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      // mutate config for production...
    } else {
      // mutate for development...
      config.devtool = "source-map";
    }
  },
  chainWebpack: (config) => {
    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "../webpack-stats.json" }]);

    config.output.filename("static/bundle.js");

    config.optimization.splitChunks(false);

    config.resolve.alias.set("__STATIC__", "static");
    // config.module.rule('images').use('url-loader')
    // .loader('file-loader') // replaces the url-loader
    // .tap(options => Object.assign(options, {
    //   name: 'static/img/[name].[hash:8].[ext]'
    // }))
    // config.module.rule('fonts').use('url-loader')
    // .loader('file-loader') // replaces the url-loader
    // .tap(options => Object.assign(options, {
    //   name: 'static/fonts/[name].[hash:8].[ext]'
    // }))

    // config.devServer
    // the first 3 lines of the following code have been added to the configuration
    // .public("http://127.0.0.1:8000")
    // .host("127.0.0.1:8000")
    // .port(800)
    // .hotOnly(true)
    // .watchOptions({ poll: 1000 })
    // .https(false)
    // .disableHostCheck(true)
    // .headers({ "Access-Control-Allow-Origin": ["*"] });
  },

  // uncomment before executing 'npm run build'
  css: {
    extract: {
      filename: "static/bundle.css",
      chunkFilename: "static/bundle.css",
    },
  },
};
