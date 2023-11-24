odoo.define('auto_save_form_view.auto_save', function (require) {
"use strict";

var core = require('web.core');
var FormController = require('web.FormController');
var worker_script = require('auto_save_form.worker_save');
var _t = core._t;

FormController.include({

    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        var self = this;
        this.saveWorker = new Worker(worker_script);
        this.auto_save_timer = 30; //seconds
        this.auto_save_new_form = false;
        this.auto_save_any_state = false;

        this._rpc({
                route: '/auto_save/data',
            }).then(function (data) {
                 if (!isNaN(parseFloat(data.save_timer))) {
                    self.auto_save_timer = parseFloat(data.save_timer);
                    self.auto_save_new_form = data.auto_save_new_form === "True" ? true : false;
                    self.auto_save_any_state = data.auto_save_any_state === "True" ? true : false;
                }
            });

        this.saveWorker.onmessage = ({ data: { } }) => {
            self.autoSave();
        };
    },

    start: async function () {
        await this._super(...arguments);
        if (this.mode === 'edit') {
            this.saveWorker.postMessage({ turn: "on", timer: this.auto_save_timer });
        }
    },

    willRestore: function () {
        this._super(...arguments);
        if (this.mode === 'edit') {
            this.saveWorker.postMessage({ turn: "on", timer: this.auto_save_timer });
        }
    },

    autoSave: function () {
        var self = this;

        if (this.mode !== 'edit') {
            this.saveWorker.postMessage({ turn: "off" });
            return;
        }

        if (!this.model.isDirty(this.handle)) {
            return;
        }

        var isAutoSave = false;

        if (this.model.isNew(this.handle) && this.auto_save_new_form) {
            isAutoSave = true;
        }
        else if(!this.model.isNew(this.handle)) {
            var record = this.model.localData[this.handle]

            if (!record.data.hasOwnProperty('state')) {
                isAutoSave = true;
            }
            else {
                if (this.auto_save_any_state) {
                    isAutoSave = true;
                }
                else if (record.data.state == 'draft') {
                    isAutoSave = true;
                }
            }
        }
        if (isAutoSave) {
            var ops = {
                stayInEdit: true,
                reload: true,
                savePoint: false,
            }
            this.saveRecord(this.handle, ops).then(function (changedFields) {
                if (changedFields.length > 0) {
                    self.displayNotification({
                        type: 'success',
                        message: _t("Form was saved automatically."),
                        sticky: false,
                    });
                }
            });
        }
    },

    _onCreate: function () {
        this._super(...arguments);
        this.saveWorker.postMessage({ turn: "on", timer: this.auto_save_timer });
    },

    _onEdit: function () {
        this._super(...arguments);
        this.saveWorker.postMessage({ turn: "on", timer: this.auto_save_timer });
    },

    _onDiscard: function () {
        this._super(...arguments);
        this.saveWorker.postMessage({ turn: "off" });
    },

    _onSave: function (ev) {
        this._super(...arguments);
        if (this.mode === 'edit') {
            this.saveWorker.postMessage({ turn: "off" });
        }
    },


});



});
