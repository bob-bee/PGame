// Configuration for your app
// https://v2.quasar.dev/quasar-cli-vite/quasar-config-file

import { defineConfig } from "#q-app";

export default defineConfig((/* ctx */) => {
  return {
    // https://v2.quasar.dev/quasar-cli-vite/prefetch-feature
    // preFetch: true,

    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://v2.quasar.dev/quasar-cli-vite/boot-files
    boot: ['axios'], // Add 'axios' to the boot array

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#css
    css: ["app.scss"],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: [
      // 'ionicons-v4',
      // 'mdi-v7',
      // 'fontawesome-v7',
      // 'eva-icons',
      // 'themify',
      // 'line-awesome',
      // 'roboto-font-latin-ext', // this or either 'roboto-font', NEVER bo[2D[K
bo[2D[K
both!

      "roboto-font", // optional, you are not bound to it
      "material-icons" // optional, you are not bound to it
    ],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#build
    build: {
      target: {
        // browser: 'baseline-widely-available',
        // node: 'node22'
      },

      typescript: {
        strict: true,
        vueShim: true
        // extendTsConfig (tsConfig) {}
      },

      // https://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-router[66D[K
https://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-router[66D[K
https://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-router#filenamehttps://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-router#filenamehttps://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-routerfilename-bttps://v2.quasar.dev/quasar-cli-vite/page-routing-with-vue-routerfilename-based-routing
      filenameBasedRouting: true,

      vueRouterMode: "hash" // available values: 'hash', 'history'
      // vueRouterBase,
      // vueDevtools,

      publicPath: '/',
      define: {
        'process.env.API_URL': process.env.API_URL || 'http://localhost:800[21D[K
'http://localhost:8000' // Configure the env build block with a dynamic API[3D[K
API_URL pointing to process.env.API_URL || 'http://localhost:8000'
      },
      defineEnv: {}

      // ignorePublicFolder: true,
      // minify: false,
      // distDir

      // extendViteConf (viteConf) {},
      // viteVuePluginOptions: {},

      // vitePlugins: [
      //   [ 'package-name', { ..pluginOptions.. }, { server: true, client:[7D[K
client:[7D[K
client: true } ]
      // ]
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#devserver
    devServer: {
      // https: true,
      host: '0.0.0.0', // Exposes the server to traffic outside the contain[7D[K
contain[7D[K
container (Docker host)
      port: 9000,
      open: false      // Stops the container from attempting to open a bro[3D[K
bro[3D[K
browser tab headlessly
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#framework
    framework: {
      config: {},

      // iconSet: 'material-icons', // Quasar icon set
      // lang: 'en-US', // Quasar language pack

      // For special cases outside of where the auto-import strategy can ha[2D[K
ha[2D[K
have an impact
      // (like functional components as one of the examples),
      // you can manually specify Quasar components/directives to be availa[6D[K
availa[6D[K
available everywhere:
      //
      // components: [],
      // directives: [],

      // Quasar plugins
      plugins: []
    },

    // animations: 'all', // --- includes all animations
    // https://v2.quasar.dev/options/animations
    animations: [],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#sourcefiles[68D[K
https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#sourcefiles[68D[K
https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#sourcefiles
    // [K
sourceFiles: {
    //   rootComponent: 'src/App.vue',
    //   router: 'src/router/index',
    //   store: 'src/store/index',
    //   pwaRegisterServiceWorker: 'src-pwa/register-sw',
    //   pwaServiceWorker: 'src-pwa/sw/custom-sw',
    //   pwaManifestFile: 'src-pwa/manifest.json',
    //   electronMain: 'src-electron/electron-main',
    //   electronPreload: 'src-electron/electron-preload'
    //   bexManifestFile: 'src-bex/manifest.json
    // },

    // https://v2.quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr
    ssr[3D[K
ssr: {
      prodPort: 3000, // The default port that the production server should[6D[K
should[6D[K
should use
      // (gets superseded if process.env.PORT is specified at runtime)

      middlewares: [
        "render" // keep this as last one
      ],

      // extendSSRPackageJson (pkgJson) {},
      // extendSSRWebserverConf (rolldownConf) {},

      // manualStoreSerialization: true,
      // manualStoreSsrContextInjection: true,
      // manualStoreHydration: true,
      // manualPostHydrationTrigger: true,

      pwa: false
      // pwaOfflineHtmlFilename: 'offline.html', // do NOT use index.html a[1D[K
a[1D[K
as name!

      // extendSSRGenerateSWOptions (cfg) {},
      // extendSSRInjectManifestOptions (cfg) {}
    },

    // https://v2.quasar.dev/quasar-cli-vite/developing-pwa/configuring-pwa[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-pwa/configuring-pwa[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-pwa/configuring-pwa
    pwa[3D[K
pwa: {
      workboxMode: "GenerateSW" // 'GenerateSW' or 'InjectManifest'
      // swFilename: 'sw.js',
      // manifestFilename: 'manifest.json',
      // extendPWAManifestJson (json) {},
      // useCredentialsForManifestTag: true,
      // injectPWAMetaTags: false,
      // extendPWACustomSWConf (rolldownConf) {},
      // extendPWAGenerateSWOptions (cfg) {},
      // extendPWAInjectManifestOptions (cfg) {},
      // extendPWAInstallPrompt (promptEvent) {}
    },

    // https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/[68D[K
https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/configuhttps://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/configuhttps://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/onfigurittps://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/onfiguring-bex
    bex: {
      // extendBexScriptsConf (rolldownConf) {},
      // extendBexManifestJson (json) {},

      /**
       * The list of extra scripts (js/ts) not in your bex manifest that yo[2D[K
yo[2D[K
you want to
       * compile and use in your browser extension. Maybe dynamic use them?[5D[K
them?[5D[K
them?
       *
       * Each entry in the list should be a relative filename to /src-bex/
       *
       * @example [ 'my-script.ts', 'sub-folder/my-other-script.js' ]
       */
      extraScripts: []
    }
  };
});