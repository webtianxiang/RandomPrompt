import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "TX.BatchPromptMenu",
  setup() {
    const menu = document.querySelector(".comfy-menu");
    const separator = document.createElement("hr");

    separator.style.margin = "20px 0";
    separator.style.width = "100%";
    menu.append(separator);

    const BatchPromptButton = document.createElement("button");
    BatchPromptButton.textContent = "Tx Batch Prompt";
    BatchPromptButton.onclick = () => {
      for (let i = 0; i < 3; i++) {
        app.queuePrompt(0, this.batchCount);
      }
      alert("Tx Batch Prompt 10");
    };
    menu.append(BatchPromptButton);
  },
});
