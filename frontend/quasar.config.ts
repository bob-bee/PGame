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

      filenameBasedRouting: true,

      vueRouterMode: "hash",
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
client:[7D[K
client: true } ]
      // ]
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#devserver
    devServer: {
      // https: true,
      host: '0.0.0.0',
      port: 9000,
      open: false
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#framework
    framework: {
      config: {},

      iconSet: 'material-icons', // Quasar icon set
      lang: 'en-US', // Quasar language pack

      components: [],
      directives: [],

      plugins: []
    },

    animations: [],

    sou[3D[K
sourceFiles: {
      rootComponent: 'src/App.vue',
      router: 'src/router/index',
      store: 'src/store/index',
      pwaRegisterServiceWorker: 'src-pwa/register-sw',
      pwaServiceWorker: 'src-pwa/sw/custom-sw',
      pwaManifestFile: 'src-pwa/manifest.json',
      electronMain: 'src-electron/electron-main',
      electronPreload: 'src-electron/electron-preload'
    },

    ssr[3D[K
ssr: {
      prodPort: 3000,
      middlewares: [
        "render"
      ],

      extendSSRPackageJson (pkgJson) {},
      extendSSRWebserverConf (rolldownConf) {},

      pwa: false
    },

    pwa[3D[K
pwa: {
      workboxMode: "GenerateSW"
    },

    bex: {
      extraScripts: []
    }
  };
});