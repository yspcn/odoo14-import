from odoo import models, fields, api
from odoo import tools

class PosSaleReport(models.Model):
    _inherit = "report.all.channels.sales"
    

    alcohol_text = fields.Boolean(string ='Alcohol', readonly=True)


    def _so(self):
        so_str = """
                SELECT sol.id AS id,
                    so.name AS name,
                    so.x_studio_alcohol as alcohol_text,
                    so.partner_id AS partner_id,
                    sol.product_id AS product_id,
                    pro.product_tmpl_id AS product_tmpl_id,
                    so.date_order AS date_order,
                    so.user_id AS user_id,
                    pt.categ_id AS categ_id,
                    so.company_id AS company_id,
                    sol.price_total / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END AS price_total,
                    so.pricelist_id AS pricelist_id,
                    rp.country_id AS country_id,
                    sol.price_subtotal / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END AS price_subtotal,
                    (sol.product_uom_qty / u.factor * u2.factor) as product_qty,
                    so.analytic_account_id AS analytic_account_id,
                    so.team_id AS team_id

            FROM sale_order_line sol
                    JOIN sale_order so ON (sol.order_id = so.id)
                    LEFT JOIN product_product pro ON (sol.product_id = pro.id)
                    JOIN res_partner rp ON (so.partner_id = rp.id)
                    LEFT JOIN product_template pt ON (pro.product_tmpl_id = pt.id)
                    LEFT JOIN product_pricelist pp ON (so.pricelist_id = pp.id)
                    LEFT JOIN uom_uom u on (u.id=sol.product_uom)
                    LEFT JOIN uom_uom u2 on (u2.id=pt.uom_id)
            WHERE so.state in ('sale','done')
        """
        return so_str

    def _from(self):
        return """(%s)""" % (self._so())

    def get_main_request(self):
        request = """
            CREATE or REPLACE VIEW %s AS
                SELECT id AS id,
                    name,
                    x_studio_alcohol,
                    partner_id,
                    product_id,
                    product_tmpl_id,
                    date_order,
                    user_id,
                    categ_id,
                    company_id,
                    price_total,
                    pricelist_id,
                    analytic_account_id,
                    country_id,
                    team_id,
                    price_subtotal,
                    product_qty
                FROM %s
                AS foo""" % (self._table, self._from())
        return request
