const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  lintOnSave: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''  
        }
      },
    },
    client: {
      overlay: false,
    },
    port: 8080
  }
})
