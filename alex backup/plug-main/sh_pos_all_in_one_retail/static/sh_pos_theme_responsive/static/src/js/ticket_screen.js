odoo.define("sh_pos_theme_responsive.ticket_screen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const TicketScreen = require("point_of_sale.TicketScreen");

    const PosTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            constructor() {
                super(...arguments);
                var self = this;

                setTimeout(() => {
                    var owl = $('#owl-ricket-demo');
                    owl.owlCarousel({
                        loop: false,
                        nav: true,
                        margin: 10,
                        responsive: {
                            0: {
                                items: 1
                            },
                            600: {
                                items: 3
                            },
                            960: {
                                items: 5
                            },
                            1200: {
                                items: 5
                            }
                        }
                    });
                    owl.on('mousewheel', '.owl-stage', function (e) {
                        if (e.originalEvent.wheelDelta > 0) {
                            owl.trigger('next.owl');
                        } else {
                            owl.trigger('prev.owl');
                        }
                        e.preventDefault();
                    });
                }, 20);


            }
            mounted() {
                super.mounted()
                if (this.env.isMobile) {

                    $('.pos-content').addClass('sh_client_pos_content')
                    $('.sh_product_management').addClass('hide_cart_screen_show')
                    $('.sh_cart_management').addClass('hide_product_screen_show')
                }
            }
        };

    Registries.Component.extend(TicketScreen, PosTicketScreen);

});