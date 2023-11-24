odoo.define("sh_pos_customer_create_offline.Models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var DB = require("point_of_sale.DB");
    const { Gui } = require("point_of_sale.Gui");
    var exports = {};
    const rpc = require("web.rpc");
    var utils = require('web.utils');
    var round_pr = utils.round_precision;

    exports.CustomerModel = Backbone.Model.extend({
        initialize: function (attributes, options) {
            Backbone.Model.prototype.initialize.apply(this, arguments);
            var self = this;
            options = options || {};
            this.pos = options.pos;
            this.currunt_client = {}
            if (options.json) {
                this.init_from_JSON(options.json);
            } else {
                this.sequence_number = this.pos.pos_session.sequence_number++;
                this.uid = this.generate_unique_id();
            }
            return this;
        },
        generate_unique_id: function () {
            // Generates a public identification number for the order.
            // The generated number must be unique and sequential. They are made 12 digit long
            // to fit into EAN-13 barcodes, should it be needed

            function zero_pad(num, size) {
                var s = "" + num;
                while (s.length < size) {
                    s = "0" + s;
                }
                return s;
            }
            return zero_pad(this.pos.pos_session.id, 5) + "-" + zero_pad(this.pos.pos_session.login_number, 3) + "-" + zero_pad(this.sequence_number, 4);
        },
        init_from_JSON: function (json) {
            if (json.pos_session_id !== this.pos.pos_session.id) {
                this.sequence_number = this.pos.pos_session.sequence_number++;
            } else {
                this.sequence_number = json.sequence_number;
                this.pos.pos_session.sequence_number = Math.max(this.sequence_number + 1, this.pos.pos_session.sequence_number);
            }
        },
        set_customer: function (dic) {
            this.currunt_client = dic
        },
        get_currunt_customer: function () {
            return this.currunt_client;
        },
        export_as_JSON: function () {
            var self = this;
            var state_id = [this.currunt_client['state_id'], self.pos.db.states_by_id[this.currunt_client['state_id']].name] || ""
            var country = [this.currunt_client['country_id'], self.pos.db.country_by_id[this.currunt_client['country_id']].name] || ""
            var address = (this.currunt_client.street ? this.currunt_client.street + ', ' : '') +
                (this.currunt_client.zip ? this.currunt_client.zip + ', ' : '') +
                (this.currunt_client.city ? this.currunt_client.city + ', ' : '') +
                (state_id ? state_id[1] + ', ' : '') +
                (country ? country[1] : '');
            return {
                currunt_client: this.currunt_client,
                uid: this.uid,
                cid: this.cid,
                address: address,
                id: this.cid,
                image_1920: this.currunt_client['image_1920'] || "",
                barcode: this.currunt_client['barcode'] || "",
                city: this.currunt_client['city'] || "",
                country_id: country,
                email: this.currunt_client['email'] || "",
                // phone: this.currunt_client['phone'] || "",
                state_id: state_id,
                street: this.currunt_client['street'] || "",
                zip: this.currunt_client['zip'] || "",
                name: this.currunt_client['name'],
                property_product_pricelist: [self.pos.default_pricelist.id, self.pos.default_pricelist.name],
                sequence_number: this.sequence_number,
            };
        },
        export_for_printing: function () {
            var self = this;
        },
    });
    DB.include({
        init: function (options) {
            this._super(options);
            this.sh_all_customers = [];
            this.old_customer_changes = [];
            this.country_by_id = {}
            this.states_by_id = {}
        },
        get_partners_sorted: function (max_count) {
            var res = this._super(max_count)
            var self = this;
            if (this.sh_all_customers.length > 0) {
                for (var i = 0; i < this.sh_all_customers.length; i++) {
                    res.unshift(self.sh_all_customers[i])
                }
            }
            return res
        },
        get_offline_clients: function () {
            return this.load('offline_clinets', [])
        },
        remove_order: function (order_id) {
            this._super(order_id)
            this.save('offline_clinets', []);
        },
        update_customer: function (dic) {
            var new_lst = []
            var self = this;
            _.each(this.sh_all_customers, function (each) {
                if (each['cid'] == dic['cid']) {
                    new_lst.push(dic)

                } else {
                    new_lst.push(each)
                }
            })
            this.sh_all_customers = new_lst
        },
        get_partner_by_cid: function (cid) {
            return this.partner_by_id[cid]
        },

        get_all_customers: function () {
            return this.sh_all_customers;
        },
        remove_sh_all_customers: function () {
            this.save('offline_clinets', []);
            this.sh_all_customers = [];
        },
        get_customer_by_cid: function (cid) {
            var all_customer = this.sh_all_customers;
            var result = []
            for (var i = 0, len = all_customer.length; i < len; i++) {
                var each_customer = all_customer[i];
                if (each_customer["cid"] == cid) {
                    result.push(each_customer)
                }
            }
            return result
        },
    });

    var CustomerCollection = Backbone.Collection.extend({
        model: exports.CustomerModel,
    });


    var OrderCollection = Backbone.Collection.extend({
        model: exports.Order,
    });

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            this.set({
                'synch': { status: 'connected', pending: 0 },
                'orders': new OrderCollection(),
                'Customers': new CustomerCollection(),
                'selectedcustomer': null,
                'selectedOrder': null,
                'selectedClient': null,
                'cashier': null,
                'selectedCategoryId': null,
            });
            _super_posmodel.initialize.call(this, session, attributes);
        },
        after_load_server_data: function () {
            var self = this
            var res = _super_posmodel.after_load_server_data.call(this, arguments)
            if (this.countries) {
                _.each(this.countries, function (each_country) {
                    self.db.country_by_id[each_country.id] = each_country
                })
            }
            if (this.states) {
                _.each(this.states, function (each_states) {
                    self.db.states_by_id[each_states.id] = each_states
                })
            }
            if(self.config.sh_allow_to_pay_order && self.config.sh_partial_pay_product_id && self.config.sh_partial_pay_product_id[0]){
                if(self.db && !self.db.get_product_by_id(self.config.sh_partial_pay_product_id[0])){
                    rpc.query({
                        model: "product.product",
                        method: "search_read",
                        fields: ['display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
                        'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
                        'product_tmpl_id','tracking', 'write_date', 'available_in_pos', 'attribute_line_ids', 'active'],
                        domain: [['id', '=', self.config.sh_partial_pay_product_id[0]]],
                    }).then(function (products) {
                        if(products && products.length > 0){
                            var using_company_currency = self.config.currency_id[0] === self.company.currency_id[0];
                            var conversion_rate = self.currency.rate / self.company_currency.rate;
                            self.db.add_products(_.map(products, function (product) {
                                if (!using_company_currency) {
                                    product.lst_price = round_pr(product.lst_price * conversion_rate, self.currency.rounding);
                                }
                                product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
                                product.pos = self;
                                return new models.Product({}, product);
                            }));
                        }
                    })
                }
            }
            return res
        },
        add_new_customer: function (options) {
            var customer = new exports.CustomerModel({}, { pos: this });
            // customer['cid'] = _.uniqueId('c');
            this.get("Customers").add(customer);
            this.set("selectedcustomer", customer, options);

            return customer;
        },
        set_customer: function (customer, options) {
            this.set({ selectedcustomer: customer }, options);
        },

        get_customer: function () {
            return this.get('selectedcustomer')
        },
        update_old_customer: function () {
            var self = this;
            _.each(this.env.pos.db.old_customer_changes, function (client) {
                self.rpc({
                    model: 'res.partner',
                    method: 'pos_write_customer',
                    args: [this, client],
                }).then(async function (client) {
                    await self.env.pos.load_new_partners();
                }).catch(function (reason) {
                    Gui.showPopup('ErrorPopup', {
                        title: 'Offline',
                        body: 'When you online Customer will be Update automiatically.',
                    });
                    self.set_synch(self.get("failed") ? "error" : "disconnected", self.env.pos.db.get_all_customers().length);
                });
            })
        },
        create_offline_clients: function () {
            var self = this;

            return new Promise(function (resolve, reject) {
                self.rpc({
                    model: 'res.partner',
                    method: 'create_offline_customer',
                    args: [self.db.get_offline_clients()],
                }, {
                    timeout: 3000,
                    shadow: true,
                }).then(async function (client_id) {
                    if (client_id.length > 0) {
                        for (var i = 0; i < client_id.length; i++) {
                            var cust = client_id[i]
                            self.env.pos.db.partner_by_id[cust['old_customer']['cid']] = cust['old_customer']
                            self.env.pos.partners.push(cust['old_customer'])
                        }
                    }
                    resolve();
                }, function (type, err) {
                    reject();
                })
            });
        }
    });


});
