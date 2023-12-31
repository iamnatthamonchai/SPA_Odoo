/** @odoo-module **/

import { getActionManagerServerData, doAction } from "@web/../tests/webclient/helpers";
import { homeMenuService } from "@web_enterprise/webclient/home_menu/home_menu_service";
import { ormService } from "@web/core/orm_service";
import { enterpriseSubscriptionService } from "@web_enterprise/webclient/home_menu/enterprise_subscription_service";
import { registry } from "@web/core/registry";
import { createEnterpriseWebClient } from "../helpers";
import { click, legacyExtraNextTick, getFixture } from "@web/../tests/helpers/utils";

const serviceRegistry = registry.category("services");

QUnit.module("WebClient Mobile", (hooks) => {
    let serverData;
    hooks.beforeEach(() => {
        serverData = getActionManagerServerData();
        serviceRegistry.add("home_menu", homeMenuService);
        serviceRegistry.add("orm", ormService);
        serviceRegistry.add("enterprise_subscription", enterpriseSubscriptionService);
    });

    QUnit.test("scroll position is kept", async (assert) => {
        // This test relies on the fact that the scrollable element in mobile
        // is the html node.
        assert.expect(6);

        const record = serverData.models.partner.records[0];
        serverData.models.partner.records = [];

        for (let i = 0; i < 80; i++) {
            const rec = Object.assign({}, record);
            rec.id = i + 1;
            rec.display_name = `Record ${rec.id}`;
            serverData.models.partner.records.push(rec);
        }

        // force the html node to be scrollable element
        const target = getFixture();
        target.style.position = "initial";
        const webClient = await createEnterpriseWebClient({ serverData });

        await doAction(webClient, 3); // partners in list/kanban
        assert.containsOnce(target, ".o_kanban_view");

        window.scrollTo(0, 123);
        await click(target.querySelectorAll(".o_kanban_record")[20]);
        await legacyExtraNextTick();
        assert.containsOnce(target, ".o_form_view");
        assert.containsNone(target, ".o_kanban_view");

        window.scrollTo(0, 0);
        await click(target.querySelector(".o_control_panel .o_back_button"));
        await legacyExtraNextTick();
        assert.containsNone(target, ".o_form_view");
        assert.containsOnce(target, ".o_kanban_view");

        assert.strictEqual(document.firstElementChild.scrollTop, 123);
    });
});
