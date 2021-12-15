script_count_pages = """
        function main(splash)
            local url = splash.args.url
            splash.response_body_enabled = false
            splash.private_mode_enabled = false
            splash.images_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
            products = splash:jsfunc([[
            function () {
                var all_rproducts = window.productsTotalCount;
                var products_on_page = window.productsPerServerPage;
                return [all_rproducts,products_on_page];
                }
             ]])
               assert(splash:go(url))
          return (
            products()
        )
        end
        """


script_url_poducts = """
    function main(splash)
            local url = splash.args.url
            splash.response_body_enabled = false
            splash.private_mode_enabled = false
            splash.images_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
            products = splash:jsfunc([[
            function () {
                var all_rproducts = window.products;
                return all_rproducts;
                }
             ]])
               assert(splash:go(url))
          return (
            products()
        )
        end
"""