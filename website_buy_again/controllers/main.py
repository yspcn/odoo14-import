# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['''/buy_again''',
                '''/buy_again/page/<int:page>''',
                '''/buy_again/category/<model("product.public.category"):category>''',
                '''/buy_again/category/<model("product.public.category"):category>/page/<int:page>'''], type="http", website=True, auth="public", sitemap=lambda x: self.sitemap_shop)
    def buy_again(self, page=0, category=None, search='', ppg=False, **post):
        res  = self.shop(page, category, search, ppg)
        orders = request.env.user.partner_id.sale_order_ids.filtered(lambda l: l.website_id == request.website and l.state in ('sale', 'done'))
        cur_user = request.env.user
        buy_again_config = request.env['buy.again.config'].search([('set_active', '=', True),('website_id','=',request.website.id)], limit=1)
        purchased_products = []
        for ord in orders:
            for p in ord.order_line:
                if not len(buy_again_config) or not buy_again_config.from_date:
                    purchased_products.append(p.product_id.product_tmpl_id.id)
                else:
                    if buy_again_config.from_date:
                        if ord.date_order >= buy_again_config.from_date:
                            purchased_products.append(p.product_id.product_tmpl_id.id)

        purchased_products = list(set(purchased_products))
        if len(buy_again_config):
            if buy_again_config.product_limit:
                purchased_products = purchased_products[:buy_again_config.product_limit]

        if category:
            url = "/buy_again/category/%s" % slug(category)

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4
        url = "/buy_again"

        Product = request.env['product.template'].with_context(bin_size=True)
        pager = request.website.pager(url=url, total=len(purchased_products), page=page, step=ppg, scope=5, url_args=post)
        products = Product.search([('id','in', purchased_products)], limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        res.qcontext['pager'] = pager
        res.qcontext['products'] = products
        res.qcontext['bins'] = TableCompute().process(products, ppg, ppr)
        res.qcontext['keep'] = QueryURL('/buy_again')
        return res
