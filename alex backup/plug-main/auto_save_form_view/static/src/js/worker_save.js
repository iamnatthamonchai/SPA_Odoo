odoo.define('auto_save_form.worker_save', function (require) {
    const workercode = () => {
      let timerInterval;
      self.onmessage = function ({ data: { turn, timer } }) {
        if (turn === "off" || timerInterval) {
            clearInterval(timerInterval);
        }
        if (turn === "on") {
            clearInterval(timerInterval);

            timerInterval = setInterval(() => {
            self.postMessage({  });
          }, timer * 1000);
        }
      };
    };

    let code = workercode.toString();
    code = code.substring(code.indexOf("{") + 1, code.lastIndexOf("}"));

    const blob = new Blob([code], { type: "application/javascript" });
    const worker_script = URL.createObjectURL(blob);

    return worker_script;
});
