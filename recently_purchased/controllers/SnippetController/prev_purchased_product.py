from odoo import http
from odoo.http import request

import logging
import operator

_logger = logging.getLogger(__name__)


class PreviousPurchasedProductsSnippet(http.Controller):
    @http.route('/shop/previously_purchased_products', auth="public", website=True, type="json")
    def purchasedProducts(self):

        # print(request.website.is_user()) # ->> returns true or false
        # print(request.website.is_public_user()) # ->> returns true or false

        orders = request.env.user.partner_id.sale_order_ids.filtered(lambda l: l.website_id == request.website and l.state in ('sale', 'done'))
        purchased_products = []
        for order in orders:
            for p in order.order_line:
                if p.product_id.product_tmpl_id.name == 'Free delivery charges':
                    pass
                else:
                    field = {'display_name': p.product_id.product_tmpl_id.name,
                             'id': p.product_id.id,
                             'list_price': p.product_id.product_tmpl_id.list_price,
                             'website_url': p.product_id.product_tmpl_id.website_url,
                             'image': request.env['website'].image_url(p.product_id, 'image_512'),
                             'quantity': p.product_uom_qty
                             }
                    purchased_products.append(field)

        _logger.info(purchased_products)

        count_ids = {}
        for i in purchased_products:
            e = i['id']
            count_ids[e] = 0

        for i in purchased_products:
            count_ids[i['id']] = i['quantity'] + count_ids[i['id']]  # all the items with their total quantities

        sorted_count_ids = dict(sorted(count_ids.items(), key=operator.itemgetter(1), reverse=True))
        _logger.info("sorted_count_ids")
        _logger.info(sorted_count_ids)

        sorted_count_ids_top_10 = {k: count_ids[k] for k in list(sorted_count_ids)[:12]}  # trimming the long list of elements

        _logger.info("sorted_count_ids_top_10")
        _logger.info(sorted_count_ids_top_10)

        unique_purchased_products = list({v['id']: v for v in purchased_products}.values())  # extracting unique products

        purchased_products = []
        for j in sorted_count_ids_top_10:
            for i in unique_purchased_products:
                if i['id'] == j:
                    field = {
                        'display_name': i['display_name'],
                        'id': i['id'],
                        'list_price': i['list_price'],
                        'website_url': i['website_url'],
                        'image': i['image'],
                    }
                    if field['display_name'] == 'Free delivery charges':
                        pass
                    else:
                        purchased_products.append(field)

        print(purchased_products)

        return http.request.env['ir.ui.view']._render_template('recently_purchased.s_previously_purchased_products_card',
                                                               {'products': purchased_products})
