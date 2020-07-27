module.exports = {
/*    publicPath: "/ui",*/
    devServer: {
        proxy: 'http://localhost:8000'
    },
    pages: {
        SignIn: {
            entry: 'src/pages/SignIn/page.ts',
            template: 'templates/index.html',
        },
        Account: {
            entry: 'src/pages/Account/page.ts',
            template: 'templates/index.html',
        }
    }
}