odoo.define('sh_pos_multiples_qty.multi_qty', function (require) {
    'use strict';

    var models = require("point_of_sale.models");
    var utils = require("web.utils");
    var round_pr = utils.round_precision;
    var field_utils = require('web.field_utils');
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { Gui } = require("point_of_sale.Gui");


    // models.load_fields("product.product", ["sh_multiples_of_qty", "sh_product_non_returnable", "sh_product_non_exchangeable","sh_product_non_returnable", "sh_product_non_exchangeable","sh_is_bundle", "sh_qty_in_bag", "is_rounding_product", "sh_secondary_uom", 'sh_is_secondary_unit', "type", "qty_available", "virtual_available", "image_1920", 'pro_min_sale_price', 'pro_max_sale_price', 'sh_select_user', 'sh_alternative_products', 'name', 'product_template_attribute_value_ids', 'weight', 'volume']);

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function (quantity, keep_price) {
            
            var self = this;

            var old_qty = 0
            if(this.quantity && quantity && this.quantity > quantity){
                old_qty = 1
            }
            if (!self.pos.is_refund_button_click ) {
            	
                if (this.pos.config.sh_update_quantity_cart_change && this.quantity) {
                    if (this && this.pos.db && this.pos.db.quant_by_product_id && this.product && this.product.id && this.pos.db.quant_by_product_id[this.product.id]) {
                        this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] = parseFloat(this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]]) + this.quantity;
                    }
                }
            }
            this.order.assert_editable();
            var quant_by_product_id = this.pos.db.quant_by_product_id[this.product.id];
            var qty_available = quant_by_product_id ? quant_by_product_id[this.pos.config.sh_pos_location[0]] : 0;
            if (quantity === 'remove') {
                if (this.refunded_orderline_id in this.pos.toRefundLines) {
                    delete this.pos.toRefundLines[this.refunded_orderline_id];
                }
                this.order.remove_orderline(this);
                return;
            } else {
                
                var quant = typeof(quantity) === 'number' ? quantity : (field_utils.parse.float('' + quantity) || 0);
                
                if (this.refunded_orderline_id in this.pos.toRefundLines) {
                    const toRefundDetail = this.pos.toRefundLines[this.refunded_orderline_id];
                    const maxQtyToRefund = toRefundDetail.orderline.qty - toRefundDetail.orderline.refundedQty
                    if (quant > 0) {
                        Gui.showPopup('ErrorPopup', {
                            title: 'Positive quantity not allowed',
                            body: 'Only a negative quantity is allowed for this refund line. Click on +/- to modify the quantity to be refunded.'
                        });
                        return false;
                    } else if (quant == 0) {
                        toRefundDetail.qty = 0;
                    } else if (-quant <= maxQtyToRefund) {
                        toRefundDetail.qty = -quant;
                    } else {
                        Gui.showPopup('ErrorPopup', {
                            title: _t('Greater than allowed'),
                            body: _.str.sprintf(
                                _t('The requested quantity to be refunded is higher than the refundable quantity of %s.'),
                                this.pos.formatProductQty(maxQtyToRefund)
                            ),
                        });
                        return false;
                    }
                }
                var unit = this.get_unit();
                if (unit) {
                    if (unit.rounding) {
                        var decimals = this.pos.dp['Product Unit of Measure'];
                        var rounding = Math.max(unit.rounding, Math.pow(10, -decimals));
                        if (this.pos.config.sh_multi_qty_enable) {
                            var qty = parseInt(this.product.sh_multiples_of_qty)
                            if (qty) {
                                if (qty <= quant) {
                                    if (quant / qty == parseInt(quant / qty)) {
                                        var loop = quant / qty
                                    } else {
                                        var loop = quant / qty + 1
                                    }
                                    for (var i = 2; i <= loop; i++) {
                                        var val = qty * i
                                        quant = val
                                    }
                                }
                                else {
                                    quant = qty
                                }
                            }
                        }


                        if (round_pr(quant, rounding) && this.pos.config.sh_show_qty_location && this.product.type == "product" && !this.product["is_added"]) {
                            var converted_qty1 = false
                            if (this.get_current_uom() && this.get_unit() != this.get_current_uom() ){
                                converted_qty1 = this.convert_qty_uom(quant, this.get_unit(), this.get_current_uom());
                                if (qty_available - round_pr(converted_qty1, rounding) >= this.pos.config.sh_min_qty) {
                                    this.quantity = round_pr(quant, rounding);
                                    this.quantityStr = field_utils.format.float(this.quantity, { digits: [69, decimals] });
                                } else {
                                    this.quantity = round_pr(0, rounding);
                                    this.quantityStr = round_pr(0, rounding);
                                    
                                    if(this.order.screen_data && Object.keys(this.order.screen_data).length > 0 ){
                                        Gui.showPopup("QuantityWarningPopup", {
                                            product: this.product,
                                            quantity: round_pr(quant, rounding),
                                            product_image: this.get_image_url(this.product.id),
                                        });
                                        
                                    }else{
                                        this.quantity = round_pr(quant, rounding);
                                        this.quantityStr = field_utils.format.float(this.quantity, { digits: [69, decimals] });
                                    }
                                }
                            }
                            else{
                                if (qty_available - round_pr(quant, rounding) >= this.pos.config.sh_min_qty) {
                                    this.quantity = round_pr(quant, rounding);
                                    this.quantityStr = field_utils.format.float(this.quantity, { digits: [69, decimals] });
                                } else {
                                    this.quantity = round_pr(0, rounding);
                                    this.quantityStr = round_pr(0, rounding);
                                    
                                    if(this.order.screen_data && Object.keys(this.order.screen_data).length > 0 ){
                                        Gui.showPopup("QuantityWarningPopup", {
                                            product: this.product,
                                            quantity: round_pr(quant, rounding),
                                            product_image: this.get_image_url(this.product.id),
                                        });
                                    }else{
                                        this.quantity = round_pr(quant, rounding);
                                        this.quantityStr = field_utils.format.float(this.quantity, { digits: [69, decimals] });
                                    }
                                }
                            }
                        } else {
                            this.quantity = round_pr(quant, rounding);
                            this.quantityStr = field_utils.format.float(this.quantity, { digits: [69, decimals] });
                            this.product["is_added"] = false;
                        }
                    } else {

                        if (round_pr(quant, rounding) && this.pos.config.sh_show_qty_location && this.product.type == "product" && !this.product["is_added"]) {
                            if (qty_available - round_pr(quant, rounding) >= this.pos.config.sh_min_qty) {
                                this.quantity = round_pr(quant, 1);
                                this.quantityStr = '' + this.quantity.toFixed(0);
                            } else {
                                this.quantity = round_pr(0, 1);    
                                this.quantityStr = '' + round_pr(0, 1);
                                Gui.showPopup("QuantityWarningPopup", {
                                    product: this.product,
                                    quantity: round_pr(quant, 1),
                                    product_image: this.get_image_url(this.product.id),
                                });
                            }
                        } else {
                            this.quantity = round_pr(quant, 1);
                            this.quantityStr = '' + this.quantity.toFixed(0);
                            this.product["is_added"] = false;
                        }
                    }
                } else {

                    if (round_pr(quant, rounding) && this.pos.config.sh_show_qty_location && this.product.type == "product" && !this.product["is_added"]) {
                        if (qty_available - round_pr(quant, rounding) >= this.pos.config.sh_min_qty) {
                            this.quantity = quant;
                            this.quantityStr = "" + this.quantity;
                        } else {
                            this.quantity = 0;
                            this.quantityStr = '0';
                            Gui.showPopup("QuantityWarningPopup", {
                                product: this.product,
                                quantity: quant,
                                product_image: this.get_image_url(this.product.id),
                            });
                        }
                    } else {
                        this.quantity = quant;
                        this.quantityStr = "" + this.quantity;
                        this.product["is_added"] = false;
                    }
                }
            }

            // just like in sale.order changing the quantity will recompute the unit price
            if (!keep_price && !this.price_manually_set) {
                this.set_unit_price(this.product.get_price(this.order.pricelist, this.get_quantity(), this.get_price_extra()));
                this.order.fix_tax_included_price(this);
            }

            var primary_uom = this.get_unit();
            if (this.pos.config.sh_enable_seconadry && this.pos.config.select_uom_type != 'secondary') {
                var secondary_uom = primary_uom;
                if (this.order.orderlines.models.includes(this)) {
                    this.is_secondary = true
                    secondary_uom = this.get_secondary_unit();
                }
            } 
            if (this.pos.config.sh_enable_seconadry && this.pos.config.select_uom_type == 'secondary') {
                this.is_secondary = true
                var secondary_uom = this.get_secondary_unit();
            }
            if (this.get_current_uom() == undefined) {
                this.set_current_uom(secondary_uom);
            }
            // // Initialization of qty when product added
            var current_uom = this.get_current_uom() || primary_uom;
            if (current_uom == primary_uom) {
                this.set_current_uom(primary_uom);
                this.set_primary_quantity(this.get_quantity());

                var converted_qty = this.convert_qty_uom(this.quantity, secondary_uom, current_uom);
                this.set_secondary_quantity(converted_qty);
                // just like in sale.order changing the quantity will recompute the unit price
                if (!keep_price && !this.price_manually_set) {
                    this.set_unit_price(this.product.get_price(this.order.pricelist, this.get_quantity()));
                    this.order.fix_tax_included_price(this);
                }
            } else {
                var converted_qty = this.convert_qty_uom(this.quantity, primary_uom, current_uom);
                this.set_primary_quantity(converted_qty);
                this.set_secondary_quantity(this.get_quantity());
                this.set_current_uom(secondary_uom);
                if (!keep_price && !this.price_manually_set && !(
                    this.pos.config.product_configurator && _.some(this.product.attribute_line_ids, (id) => id in this.pos.attributes_by_ptal_id))) {
                    this.set_unit_price(this.product.get_price(this.order.pricelist, converted_qty));
                    this.order.fix_tax_included_price(this);
                }
            }
           
            if (this.pos.config.sh_update_quantity_cart_change && !self.pos.is_refund_button_click) {
                if (this && this.pos.db && this.pos.db.quant_by_product_id && this.product && this.product.id && this.pos.db.quant_by_product_id[this.product.id]) {
                    var actual_quantity = 0.0;
                    // actual_quantity = this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] - this.quantity
                    if (this.get_unit() != this.get_current_uom()){
                        var converted_qty = this.convert_qty_uom(this.quantity, this.get_unit(), this.get_current_uom());
                        actual_quantity = this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] - converted_qty.toFixed(2)
                    }else{
                        actual_quantity = this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] - this.quantity
                        if(self.pack_lot_lines && self.pack_lot_lines.length > 0 && this.quantity == 1 && !old_qty){
                            actual_quantity = actual_quantity - 1;
                            
                        }
                    }
                    var list = { product_id: [this.product.id, this.product.display_name], location_id: this.pos.config.sh_pos_location, quantity: actual_quantity };
                    $.get(
                        "/update_quanttiy",
                        {
                            passed_list: list,
                        },
                        function (result) {}
                    );
                }
            }
            
            
            this.trigger('change', this);
            return true
        },
    });

});
