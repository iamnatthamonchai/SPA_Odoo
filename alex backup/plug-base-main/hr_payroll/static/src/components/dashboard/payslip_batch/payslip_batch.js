/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";

const { Component } = owl;

export class PayrollDashboardPayslipBatch extends Component {
    setup() {
        this.actionService = useService("action");
    }

    /**
     * Handles clicking on the title
     */
    onClickTitle() {
        this.actionService.doAction('hr_payroll.action_hr_payslip_run_tree');
    }

    getColorFromState(state) {
        const colorMap = {
            'New': 'bg-info-light',
            'Confirmed': 'bg-success-light',
            'Done': 'bg-primary-light',
            'Paid': 'bg-warning-light',
        };
        return colorMap[state] || 'badge-primary'
    }

    /**
     * Handles clicking on the line
     *
     * @param {number} batchID
     * @param {string} batchNames
     */
    onClickLine(batchID, batchName) {
        this.actionService.doAction({
            name: batchName,
            type: 'ir.actions.act_window',
            name: this.env._t('Employee Payslips'),
            res_model: 'hr.payslip.run',
            res_id: batchID,
            views: [[false, 'form']],
        });
    }
}

PayrollDashboardPayslipBatch.template = 'hr_payroll.PayslipBatch';
