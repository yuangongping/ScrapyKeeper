const path = require('path')

module.exports = {
    //打包配置
    publicPath: './',
    //svg
    chainWebpack: config => {
        const svgRule = config.module.rule('svg')
        // 清除已有的所有 loader。
        svgRule.uses.clear()
        svgRule
            .test(/\.svg$/)
            // 配置icons的目录
            .include.add(path.resolve(__dirname, './src/icons/svg'))
            .end()
            .use('svg-sprite-loader')
            .loader('svg-sprite-loader')
            .options({
                symbolId: 'icon-[name]'
            })
        const fileRule = config.module.rule('file')
        fileRule.uses.clear()
        fileRule
            .test(/\.svg$/)
            // 配置icons的目录
            .exclude.add(path.resolve(__dirname, './src/icons/svg'))
            .end()
            .use('file-loader')
            .loader('file-loader')
    }
}
